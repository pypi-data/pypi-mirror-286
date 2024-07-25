# -*- coding: utf-8 -*-
import argparse
import sys
from typing import Any

from mantis_scenario_model.node import VirtualMachine
from mantis_scenario_model.scenario_run_config_model import ScenarioRunConfig
from ruamel.yaml import YAML

from mantis_api_client import scenario_api
from mantis_api_client.oidc import oidc_client
from mantis_api_client.utils import colored
from mantis_api_client.utils import wait_lab


#
# 'topology_list_handler' handler
#
def topology_list_handler(args: Any) -> None:
    try:
        topologies = scenario_api.fetch_topologies()
    except Exception as e:
        print(colored(f"Error when fetching topologies: '{e}'", "red"))
        sys.exit(1)

    if args.json:
        print([item.dict() for item in topologies])
        return

    print("[+] Available topologies:")
    for topology in topologies:
        print(f"  [+] {topology.name}")


#
# 'topology_info_handler' handler
#
def topology_info_handler(args: Any) -> None:
    # Parameters
    topology_name = args.topology_name

    try:
        topology = scenario_api.fetch_topology_by_name(topology_name)
    except Exception as e:
        print(colored(f"Error when fetching topology {topology_name}: '{e}'", "red"))
        sys.exit(1)

    if args.json:
        print(topology.json())
        return

    print("[+] Topology information:")
    print(f"  [+] \033[1mName\033[0m: {topology.name}")
    print("  [+] \033[1mNodes\033[0m:")
    for node in topology.nodes:
        if type(node) is VirtualMachine:
            print(f"       [+] {node.type}: {node.name} ({node.basebox_id})")
        else:
            print(f"       [+] {node.type}: {node.name}")
    print("  [+] \033[1mLinks\033[0m:")
    for link in topology.links:
        print(
            f"        [+] {link.switch.name}({link.switch.type}) -- {link.params.ip} -- {link.node.name}({link.node.type})"
        )


#
# 'topology_run_handler' handler
#
def topology_run_handler(args: Any) -> None:
    # Parameters
    topology_name = args.topology_name
    scenario_run_config_path = args.scenario_run_config_path

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
        topology = scenario_api.fetch_topology_by_name(topology_name)
        print(f"[+] Going to execute topology: {topology.name}")

        lab_id = scenario_api.run_topology(topology, scenario_run_config, args.group_id)
        print(f"[+] Topology lab ID: {lab_id}")

        wait_lab(lab_id)

    except Exception as e:
        print(colored(f"Error when running topology {topology_name}: '{e}'", "red"))
        sys.exit(1)
    finally:
        print("[+] Topology execution ended")

        if args.destroy_after_scenario:
            print("[+] Stopping lab...")
            scenario_api.stop_lab(lab_id)


def add_topology_parser(
    root_parser: argparse.ArgumentParser,
    subparsers: Any,
    group_required: bool,
) -> None:
    # -------------------
    # --- Scenario API options (topologies)
    # -------------------

    parser_topology = subparsers.add_parser(
        "topology",
        help="Scenario API related commands (topology)",
        formatter_class=root_parser.formatter_class,
    )
    subparsers_topology = parser_topology.add_subparsers()

    # 'topology_list' command
    parser_topology_list = subparsers_topology.add_parser(
        "list",
        help="List all available topologies",
        formatter_class=root_parser.formatter_class,
    )
    parser_topology_list.set_defaults(func=topology_list_handler)
    parser_topology_list.add_argument(
        "--json", help="Return JSON result.", action="store_true"
    )

    # 'topology_info' command
    parser_topology_info = subparsers_topology.add_parser(
        "info",
        help="Get information about a topology",
        formatter_class=root_parser.formatter_class,
    )
    parser_topology_info.set_defaults(func=topology_info_handler)
    parser_topology_info.add_argument(
        "topology_name", type=str, help="The topology name"
    )
    parser_topology_info.add_argument(
        "--json", help="Return JSON result.", action="store_true"
    )

    # 'topology_run' command
    parser_topology_run = subparsers_topology.add_parser(
        "run",
        help="Run a specific topology",
        formatter_class=root_parser.formatter_class,
    )
    parser_topology_run.set_defaults(func=topology_run_handler)
    parser_topology_run.add_argument(
        "topology_name", type=str, help="The topology name"
    )
    parser_topology_run.add_argument(
        "--destroy",
        action="store_true",
        dest="destroy_after_scenario",
        help="Do not keep the lab up after topology execution (False by default)",
    )
    parser_topology_run.add_argument(
        "group_id",
        metavar="group-id",
        type=str,
        nargs=1 if group_required else "?",
        default=oidc_client.get_default_group(raise_exc=False),
        help="The group ID that have ownership on lab (default: %(default)s)",
    )
    parser_topology_run.add_argument(
        "--scenario_run_config",
        action="store",
        required=False,
        dest="scenario_run_config_path",
        help="Input path of a YAML configuration for the scenario run",
    )

    parser_topology.set_defaults(func=lambda _: parser_topology.print_help())
