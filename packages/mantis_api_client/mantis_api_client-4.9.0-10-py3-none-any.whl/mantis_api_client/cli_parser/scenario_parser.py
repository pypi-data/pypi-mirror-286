# -*- coding: utf-8 -*-
import argparse
import sys
import traceback
from typing import Any

from mantis_scenario_model.scenario_run_config_model import ScenarioRunConfig
from ruamel.yaml import YAML

from mantis_api_client import scenario_api
from mantis_api_client.oidc import oidc_client
from mantis_api_client.utils import colored
from mantis_api_client.utils import wait_lab


#
# 'scenario_list_handler' handler
#
def scenario_list_handler(args: Any) -> None:
    try:
        scenarios = scenario_api.fetch_scenarios()
    except Exception as e:
        print(colored(f"Error when fetching scenarios: '{e}'", "red"))
        sys.exit(1)

    if args.json:
        print([item.dict() for item in scenarios])
        return

    print(f"[+] Available scenarios ({len(scenarios)}):")
    for scenario in scenarios:
        print(f"  [+] \033[1m{scenario.name}\033[0m")
        print(f"         {scenario.description}")


#
# 'scenario_info_handler' handler
#
def scenario_info_handler(args: Any) -> None:
    # Parameters
    scenario_name = args.scenario_name

    try:
        scenario = scenario_api.fetch_scenario_by_name(scenario_name)
    except Exception as e:
        print(
            colored(
                f"Error when fetching scenario {scenario_name}: '{e}'",
                "red",
                "on_white",
            )
        )
        sys.exit(1)

    if args.json:
        print(scenario.json())
        return

    print("[+] Scenario information:")
    print(f"  [+] \033[1mName\033[0m: {scenario.name}")
    print("  [+] \033[1mKeywords\033[0m: ", end="")
    print(", ".join(scenario.keywords))
    print(f"  [+] \033[1mDescription\033[0m: {scenario.description}")
    if len(scenario.long_description) > 0:
        print("  [+] \033[1mLong description\033[0m:")
        for ld in scenario.long_description:
            print(f"        - {ld}")
    print("  [+] \033[1mAvailable scenario config\033[0m:")
    for config in scenario.scenario_config:
        if config.get("initial_target_name", None):
            target = f", target: {config.get('initial_target_name', None)}"
        else:
            target = ""
        print(
            f"""       [+] {config.get('name', None)} (Topology: {config.get('file', None)}){target}"""
        )


#
# 'scenario_run_handler' handler
#
def scenario_run_handler(args: Any) -> None:
    # Parameters
    scenario_name = args.scenario_name
    scenario_run_config_path = args.scenario_run_config_path
    scenario_config_name = args.scenario_config_name

    # Manage scenario run configuration
    if scenario_run_config_path is None:
        scenario_run_config_dict = {}
    else:
        with open(scenario_run_config_path, "r") as fd:
            yaml_content = fd.read()
        loader = YAML(typ="rt")
        scenario_run_config_dict = loader.load(yaml_content)
    scenario_run_config = ScenarioRunConfig(**scenario_run_config_dict)

    # Launch scenario
    try:
        scenario = scenario_api.fetch_scenario_by_name(scenario_name)
        print(f"[+] Going to execute scenario: {scenario.name}")

        if scenario_config_name is None:
            print(
                "Needed argument --scenario_config_name, in order to choose the unit scenario to run"
            )
            print("Available unit scenarios:")
            for available_scenario_config in scenario.scenario_config:
                print(f"  [+] {available_scenario_config['name']}")
            sys.exit(-1)

        if scenario_config_name not in scenario.scenario_config:
            print(
                colored(
                    f"Error '{scenario_config_name}' not supported for this scenario.",
                    "red",
                    "on_white",
                )
            )
            sys.exit(-1)

        lab_id = scenario_api.run_scenario(
            scenario,
            scenario_run_config,
            args.group_id,
            scenario_config_name=scenario_config_name,
        )
        print(f"[+] Scenario lab ID: {lab_id}")

        wait_lab(lab_id)

    except Exception as e:
        print(colored(f"Error when running scenario {scenario_name}: '{e}'", "red"))
        print(traceback.format_exc())
        sys.exit(1)
    finally:
        print("[+] Scenario ended")

        if args.destroy_after_scenario:
            print("[+] Stopping lab...")
            scenario_api.stop_lab(lab_id)


def add_scenario_parser(
    root_parser: argparse.ArgumentParser,
    subparsers: Any,
    group_required: bool,
) -> None:
    # --------------------
    # --- Scenario API options (scenario)
    # --------------------

    parser_scenario = subparsers.add_parser(
        "scenario",
        help="Scenario API related commands (scenario)",
        formatter_class=root_parser.formatter_class,
    )
    subparsers_scenario = parser_scenario.add_subparsers()

    # 'scenario_list' command
    parser_scenario_list = subparsers_scenario.add_parser(
        "list",
        help="List all available scenarios",
        formatter_class=root_parser.formatter_class,
    )
    parser_scenario_list.set_defaults(func=scenario_list_handler)
    parser_scenario_list.add_argument(
        "--json", help="Return JSON result.", action="store_true"
    )

    # 'scenario_info' command
    parser_scenario_info = subparsers_scenario.add_parser(
        "info",
        help="Get information about a scenario",
        formatter_class=root_parser.formatter_class,
    )
    parser_scenario_info.set_defaults(func=scenario_info_handler)
    parser_scenario_info.add_argument(
        "scenario_name", type=str, help="The scenario name"
    )
    parser_scenario_info.add_argument(
        "--json", help="Return JSON result.", action="store_true"
    )

    # 'scenario_run' command
    parser_scenario_run = subparsers_scenario.add_parser(
        "run",
        help="Run a specific scenario",
        formatter_class=root_parser.formatter_class,
    )
    parser_scenario_run.set_defaults(func=scenario_run_handler)
    parser_scenario_run.add_argument(
        "scenario_name", type=str, help="The scenario name"
    )
    parser_scenario_run.add_argument(
        "group_id",
        metavar="group-id",
        type=str,
        nargs=1 if group_required else "?",
        default=oidc_client.get_default_group(raise_exc=False),
        help="The group ID that have ownership on lab (default: %(default)s)",
    )
    parser_scenario_run.add_argument(
        "--topology",
        action="store",
        required=False,
        dest="topology_file",
        help="Input path of a YAML topology file to override the default one",
    )
    parser_scenario_run.add_argument(
        "--destroy",
        action="store_true",
        dest="destroy_after_scenario",
        help="Do not keep the lab up after scenario execution (False by default)",
    )
    parser_scenario_run.add_argument(
        "--scenario_run_config",
        action="store",
        required=False,
        dest="scenario_run_config_path",
        help="Input path of a YAML configuration for the scenario run",
    )

    parser_scenario_run.add_argument(
        "--scenario_config_name",
        required=False,
        dest="scenario_config_name",
        help="Allows to define the scenario config to run",
    )

    parser_scenario.set_defaults(func=lambda _: parser_scenario.print_help())
