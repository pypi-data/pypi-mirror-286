# -*- coding: utf-8 -*-
import argparse
import sys
import traceback
from typing import Any

from mantis_scenario_model.scenario_run_config_model import ScenarioRunConfig
from mantis_scenario_model.unit_attack_model import Empty
from ruamel.yaml import YAML

from mantis_api_client import scenario_api
from mantis_api_client.oidc import oidc_client
from mantis_api_client.utils import colored
from mantis_api_client.utils import wait_lab


#
# 'attack_list_handler' handler
#
def attack_list_handler(args: Any) -> None:
    try:
        attacks = scenario_api.fetch_attacks()
    except Exception as e:
        print(colored(f"Error when fetching attacks: '{e}'", "red"))
        sys.exit(1)

    if args.json:
        print([item.dict() for item in attacks])
        return

    width = 35
    print(f"[+] Available attacks ({len(attacks)}):")
    name = "NAME"
    print(f"  [+] \033[1m{name: <{width}}- DESCRIPTION\033[0m")

    for attack in attacks:
        if not isinstance(attack.mitre_data.subtechnique, Empty):
            mitre_print = attack.mitre_data.subtechnique.id
        else:
            mitre_print = attack.mitre_data.technique.id

        print("  [+] ", end="")
        print(f"{attack.name: <{width}}", end="")
        print(f"- {attack.title} ({mitre_print})")


#
# 'attack_info_handler' handler
#
def attack_info_handler(args: Any) -> None:
    # Parameters
    attack_name = args.attack_name

    try:
        attack = scenario_api.fetch_attack_by_name(attack_name)
    except Exception as e:
        print(
            colored(
                f"Error when fetching attack {attack_name}: '{e}'", "red", "on_white"
            )
        )
        sys.exit(1)

    if args.json:
        print(attack.json())
        return

    print("[+] Attack information:")
    print(f"  [+] \033[1mID\033[0m: {attack.worker_id}")
    print(f"  [+] \033[1mName\033[0m: {attack.name}")
    print(f"  [+] \033[1mDescription\033[0m: {attack.description}")
    print("  [+] \033[1mAvailable scenario config\033[0m:")
    for scenario_config in attack.scenario_config:
        print(
            f"    [+] {scenario_config['name']} (Topology: {scenario_config['file']})"
        )


#
# 'attack_run_handler' handler
#
def attack_run_handler(args: Any) -> None:
    # Parameters
    attack_name = args.attack_name
    scenario_config_name = args.scenario_config_name
    scenario_run_config_path = args.scenario_run_config_path

    # Safety checks
    attack = scenario_api.fetch_attack_by_name(attack_name)
    print(f"[+] Going to execute attack: {attack.name}")

    # Safety checks
    if len(attack.scenario_config) == 0:
        print(
            f"Cannot run attack '{attack_name}', because it does not have any unit scenario"
        )
        sys.exit(-1)

    if scenario_config_name is None:
        print(
            "Needed argument --scenario_config_name, in order to choose the unit scenario to run"
        )
        print("Available unit scenarios:")
        for available_scenario_config in attack.scenario_config:
            print(f"  [+] {available_scenario_config['name']}")
        sys.exit(-1)

    for available_scenario_config in attack.scenario_config:
        if available_scenario_config["name"] == scenario_config_name:
            break
    else:
        print(f"Select scenario config '{scenario_config_name}' is not available")
        print("Available unit scenarios:")
        for available_scenario_config in attack.scenario_config:
            print(f"  [+] {available_scenario_config['name']}")
        sys.exit(-1)

    # Manage scenario run configuration
    if scenario_run_config_path is None:
        scenario_run_config_dict = {}
    else:
        with open(scenario_run_config_path, "r") as fd:
            yaml_content = fd.read()
        loader = YAML(typ="rt")
        scenario_run_config_dict = loader.load(yaml_content)
    scenario_run_config = ScenarioRunConfig(**scenario_run_config_dict)

    # Launch topology
    try:
        lab_id = scenario_api.run_attack(
            attack, scenario_config_name, scenario_run_config, args.group_id
        )

        print(f"[+] Scenario lab ID: {lab_id}")

        wait_lab(lab_id)

        print("[+] Scenario ended")
    except Exception as e:
        print(colored(f"Error when running attack {attack_name}: '{e}'", "red"))
        print(traceback.format_exc())
        sys.exit(1)
    finally:
        if args.destroy_after_scenario:
            print("[+] Stopping lab...")
            scenario_api.stop_lab(lab_id)


def add_attack_parser(
    root_parser: argparse.ArgumentParser,
    subparsers: Any,
    group_required: bool,
) -> None:
    # --------------------
    # --- Scenario API options (attack)
    # --------------------

    parser_attack = subparsers.add_parser(
        "attack",
        help="Scenario API related commands (attacks)",
        formatter_class=root_parser.formatter_class,
    )
    subparsers_attack = parser_attack.add_subparsers()

    # 'attack_list' command
    parser_attack_list = subparsers_attack.add_parser(
        "list",
        help="List all available attacks",
        formatter_class=root_parser.formatter_class,
    )
    parser_attack_list.set_defaults(func=attack_list_handler)
    parser_attack_list.add_argument(
        "--json", help="Return JSON result.", action="store_true"
    )

    # 'attack_info' command
    parser_attack_info = subparsers_attack.add_parser(
        "info",
        help="Get information about an attack",
        formatter_class=root_parser.formatter_class,
    )
    parser_attack_info.set_defaults(func=attack_info_handler)
    parser_attack_info.add_argument("attack_name", type=str, help="The attack name")
    parser_attack_info.add_argument(
        "--json", help="Return JSON result.", action="store_true"
    )

    # 'attack_run' command
    parser_attack_run = subparsers_attack.add_parser(
        "run", help="Run a specific attack", formatter_class=root_parser.formatter_class
    )
    parser_attack_run.set_defaults(func=attack_run_handler)
    parser_attack_run.add_argument("attack_name", type=str, help="The attack name")
    parser_attack_run.add_argument(
        "--destroy",
        action="store_true",
        dest="destroy_after_scenario",
        help="Do not keep the lab up after scenario execution (False by default)",
    )
    parser_attack_run.add_argument(
        "--scenario_config_name",
        dest="scenario_config_name",
        help="Allows to define the unit scenario to run for a unit attack",
    )
    parser_attack_run.add_argument(
        "group_id",
        metavar="group-id",
        type=str,
        nargs=1 if group_required else "?",
        default=oidc_client.get_default_group(raise_exc=False),
        help="The group ID that have ownership on lab (default: %(default)s)",
    )
    parser_attack_run.add_argument(
        "--scenario_run_config",
        action="store",
        required=False,
        dest="scenario_run_config_path",
        help="Input path of a YAML configuration for the scenario run",
    )

    parser_attack.set_defaults(func=lambda _: parser_attack.print_help())
