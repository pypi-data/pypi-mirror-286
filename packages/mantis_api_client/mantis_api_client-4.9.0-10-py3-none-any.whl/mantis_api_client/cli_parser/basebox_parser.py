# -*- coding: utf-8 -*-
import argparse
import json
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
# 'basebox_list_handler' handler
def basebox_list_handler(args: Any) -> None:
    try:
        baseboxes = scenario_api.fetch_baseboxes()
    except Exception as e:
        print(colored(f"Error when fetching baseboxes: '{e}'", "red"))
        sys.exit(1)

    if args.json:
        print(json.dumps(baseboxes))
        return

    print("[+] Available baseboxes:")
    for basebox in baseboxes:
        print(f"  [+] {basebox.id}")


#
# 'basebox_info_handler' handler
#
def basebox_info_handler(args: Any) -> None:
    # Parameters
    basebox_id = args.basebox_id

    try:
        basebox = scenario_api.fetch_basebox_by_id(basebox_id)
    except Exception as e:
        print(colored(f"Error when fetching basebox {basebox_id}: '{e}'", "red"))
        sys.exit(1)

    if args.json:
        print(basebox.json())
        return

    print("[+] Basebox information:")
    print(f"  [+] \033[1mId\033[0m: {basebox.id}")
    print(f"  [+] \033[1mDescription\033[0m: {basebox.description}")
    print(f"  [+] \033[1mOS\033[0m: {basebox.operating_system} ({basebox.system_type})")
    print(f"  [+] \033[1mLanguage\033[0m: {basebox.language}")
    print(f"  [+] \033[1mInstallation date\033[0m: {basebox.installation_date}")
    print("  [+] \033[1mCredentials\033[0m:")
    if basebox.username != "" and basebox.username:
        print(f"       [+] User: {basebox.username}:{basebox.password}")
    if basebox.admin_username != "" and basebox.admin_username:
        print(
            f"       [+] Administrator: {basebox.admin_username}:{basebox.admin_password}"
        )
    print("  [+] \033[1mCPE\033[0m:")
    for cpe in basebox.cpe.splitlines():
        print(f"        [+] {cpe}")
    if basebox.changelog:
        print("  [+] \033[1mChangelog\033[0m:")
        for changelog in basebox.changelog:
            if changelog.get("date", "") != "":
                print(f"""        [+] {changelog.get("date")}:""")
                for info in changelog.get("info", "").splitlines():
                    print(f"""              {info}""")


#
# 'basebox_run_handler' handler
#
def basebox_run_handler(args: Any) -> None:
    # Parameters
    basebox_id = args.basebox_id
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

    # Launch basebox
    try:
        print(f"[+] Going to execute basebox: {basebox_id}")

        lab_id = scenario_api.run_basebox(
            basebox_id, scenario_run_config, args.group_id
        )
        print(f"[+] Basebox lab ID: {lab_id}")

        wait_lab(lab_id)

    except Exception as e:
        print(colored(f"Error when running basebox {basebox_id}: '{e}'", "red"))
        print(traceback.format_exc())
        sys.exit(1)
    finally:
        print("[+] Basebox execution ended")

        if args.destroy_after_scenario:
            print("[+] Stopping lab...")
            scenario_api.stop_lab(lab_id)


def add_basebox_parser(
    root_parser: argparse.ArgumentParser,
    subparsers: Any,
    group_required: bool,
) -> None:
    # -------------------
    # --- Scenario API options (baseboxes)
    # -------------------

    parser_basebox = subparsers.add_parser(
        "basebox",
        help="Scenario API related commands (basebox)",
        formatter_class=root_parser.formatter_class,
    )
    subparsers_basebox = parser_basebox.add_subparsers()

    # 'basebox_list' command
    parser_basebox_list = subparsers_basebox.add_parser(
        "list",
        help="List all available baseboxes",
        formatter_class=root_parser.formatter_class,
    )
    parser_basebox_list.set_defaults(func=basebox_list_handler)
    parser_basebox_list.add_argument(
        "--json", help="Return JSON result.", action="store_true"
    )

    # 'basebox_info' command
    parser_basebox_info = subparsers_basebox.add_parser(
        "info",
        help="Get information about a basebox",
        formatter_class=root_parser.formatter_class,
    )
    parser_basebox_info.set_defaults(func=basebox_info_handler)
    parser_basebox_info.add_argument("basebox_id", type=str, help="The basebox ID")
    parser_basebox_info.add_argument(
        "--json", help="Return JSON result.", action="store_true"
    )

    # 'basebox_run' command
    parser_basebox_run = subparsers_basebox.add_parser(
        "run",
        help="Run a specific basebox",
        formatter_class=root_parser.formatter_class,
    )
    parser_basebox_run.set_defaults(func=basebox_run_handler)
    parser_basebox_run.add_argument("basebox_id", type=str, help="The basebox ID")
    parser_basebox_run.add_argument(
        "--destroy",
        action="store_true",
        dest="destroy_after_scenario",
        help="Do not keep the lab up after basebox execution (False by default)",
    )
    parser_basebox_run.add_argument(
        "group_id",
        metavar="group-id",
        type=str,
        nargs=1 if group_required else "?",
        default=oidc_client.get_default_group(raise_exc=False),
        help="The group ID that have ownership on lab (default: %(default)s)",
    )
    parser_basebox_run.add_argument(
        "--scenario_run_config",
        action="store",
        required=False,
        dest="scenario_run_config_path",
        help="Input path of a YAML configuration for the scenario run",
    )

    parser_basebox.set_defaults(func=lambda _: parser_basebox.print_help())
