# -*- coding: utf-8 -*-
import argparse
import json
import os
import sys
from typing import Any

import mantis_api_client.scenario_api as scenario_api
from cr_api_client.cli_parser.provisioning_parser import add_provisioning_parser
from mantis_api_client.cli_parser.redteam_parser import add_redteam_parser
from mantis_api_client.oidc import oidc_client


#
# 'lab_info_handler' handler
#
def lab_info_handler(args: Any) -> None:
    # Parameters
    lab_id = args.lab_id

    try:
        lab = scenario_api.fetch_lab(lab_id)
    except Exception as e:
        print(f"Error when fetching lab: '{e}'")
        sys.exit(1)

    if args.json:
        print(json.dumps(lab))
        return

    print("[+] Lab information:")
    print(f"""  [+] \033[1mId\033[0m: {lab.get("id", None)}""")
    print(f"""  [+] \033[1mName\033[0m: {lab.get("name", None)}""")
    print(f"""  [+] \033[1mType\033[0m: {lab.get("content_type", None)}""")
    print(f"""  [+] \033[1mStatus\033[0m: {lab.get("info", None)}""")
    print(f"""  [+] \033[1mStart time\033[0m: {lab.get("start_time", None)}""")
    time = float(lab.get("elapsed_time", "0")) / 60
    print(f"""  [+] \033[1mElapsed time (minutes)\033[0m: {round(time, 2)}""")
    print(f"""  [+] \033[1mCreated by\033[0m: {lab.get("created_by", None)}""")


#
# 'lab_api_handler' handler
#
def lab_api_handler(args: Any) -> None:
    # Parameters
    lab_id = args.lab_id

    active_profile_domain = oidc_client.get_active_profile_domain(raise_exc=False)
    if not active_profile_domain:
        print("[+] Not authenticated")
        return

    provisioning_api_url = (
        f"https://app.{active_profile_domain}/proxy/{lab_id}/api/provisioning"
    )
    redteam_api_url = f"https://app.{active_profile_domain}/proxy/{lab_id}/api/redteam"

    print("[+] Lab APIs:")
    print(f"""  [+] \033[1mProvisioning API URL\033[0m: {provisioning_api_url}""")
    print(f"""  [+] \033[1mRedteam API URL\033[0m:      {redteam_api_url}""")


#
# 'lab_stop_handler' handler
#
def lab_stop_handler(args: Any) -> None:
    # Parameters
    lab_id = args.lab_id

    try:
        scenario_api.stop_lab(lab_id)
    except Exception as e:
        print(f"Error when stopping lab: '{e}'")
        sys.exit(1)

    print(f"[+] Lab '{lab_id}' stopped")


#
# 'lab_delete_lab_handler' handler
#
def lab_delete_lab_handler(args: Any) -> None:
    # Parameters
    lab_id = args.lab_id

    try:
        scenario_api.delete_lab(lab_id)
    except Exception as e:
        print(f"Error when deleting lab ID {lab_id}: '{e}'")
        sys.exit(1)

    print(f"[+] Lab '{lab_id}' deleted")


#
# 'lab_resume_handler' handler
#
def lab_resume_handler(args: Any) -> None:
    # Parameters
    lab_id = args.lab_id

    try:
        scenario_api.resume_lab(lab_id)
    except Exception as e:
        print(f"Error when resume lab: '{e}'")
        sys.exit(1)

    print(f"[+] Lab '{lab_id}' stopped")


#
# 'lab_topology_handler' handler
#
def lab_topology_handler(args: Any) -> None:
    # Parameters
    lab_id = args.lab_id

    try:
        topology = scenario_api.fetch_lab_topology(lab_id)
    except Exception as e:
        print(f"Error when fetching scenario topology: '{e}'")
        sys.exit(1)

    print(json.dumps(topology))


#
# 'lab_nodes_handler' handler
#
def lab_nodes_handler(args: Any) -> None:
    # Parameters
    lab_id = args.lab_id

    try:
        nodes = scenario_api.fetch_lab_nodes(lab_id)
    except Exception as e:
        print(f"Error when fetching scenario nodes: '{e}'")
        sys.exit(1)

    print(json.dumps(nodes))


#
# 'lab_assets_handler' handler
#
def lab_assets_handler(args: Any) -> None:
    # Parameters
    lab_id = args.lab_id

    try:
        assets = scenario_api.fetch_lab_assets(lab_id)
    except Exception as e:
        print(f"Error when fetching scenario assets: '{e}'")
        sys.exit(1)

    print(json.dumps(assets))


#
# 'lab_attack_report_handler' handler
#
def lab_attack_report_handler(args: Any) -> None:
    # Parameters
    lab_id = args.lab_id

    try:
        attack_report = scenario_api.fetch_lab_attack_report(lab_id)
    except Exception as e:
        print(f"Error when fetching scenario attack_report: '{e}'")
        sys.exit(1)

    print(json.dumps(attack_report))


#
# 'lab_attack_infras_handler' handler
#
def lab_attack_infras_handler(args: Any) -> None:
    # Parameters
    lab_id = args.lab_id

    try:
        attack_infras = scenario_api.fetch_lab_attack_infras(lab_id)
    except Exception as e:
        print(f"Error when fetching scenario attack_infras: '{e}'")
        sys.exit(1)

    print(json.dumps(attack_infras))


#
# 'lab_attack_sessions_handler' handler
#
def lab_attack_sessions_handler(args: Any) -> None:
    # Parameters
    lab_id = args.lab_id

    try:
        attack_sessions = scenario_api.fetch_lab_attack_sessions(lab_id)
    except Exception as e:
        print(f"Error when fetching scenario attack_sessions: '{e}'")
        sys.exit(1)

    print(json.dumps(attack_sessions))


#
# 'lab_attack_knowledge_handler' handler
#
def lab_attack_knowledge_handler(args: Any) -> None:
    # Parameters
    lab_id = args.lab_id

    try:
        attack_knowledge = scenario_api.fetch_lab_attack_knowledge(lab_id)
    except Exception as e:
        print(f"Error when fetching scenario attack_knowledge: '{e}'")
        sys.exit(1)

    print(json.dumps(attack_knowledge))


#
# 'lab_notifications_handler' handler
#
def lab_notifications_handler(args: Any) -> None:
    # Parameters
    lab_id = args.lab_id

    try:
        notifications = scenario_api.fetch_lab_notifications(lab_id)
    except Exception as e:
        print(f"Error when fetching scenario notifications: '{e}'")
        sys.exit(1)

    print(json.dumps(notifications))


#
# 'lab_scenario_run_config_handler' handler
#
def lab_scenario_run_config_handler(args: Any) -> None:
    # Parameters
    lab_id = args.lab_id

    try:
        scenario_run_config = scenario_api.fetch_lab_scenario_run_config(lab_id)
    except Exception as e:
        print(f"Error when fetching scenario run config: '{e}'")
        sys.exit(1)

    print(json.dumps(scenario_run_config))


def lab_set_lab_handler(args: Any) -> None:
    # Parameters
    lab_id = args.lab_id

    active_profile_domain = oidc_client.get_active_profile_domain(raise_exc=False)
    if not active_profile_domain:
        print("[+] Not authenticated")
        return

    os.environ["PROVISIONING_API_URL"] = (
        f"https://app.{active_profile_domain}/proxy/{lab_id}/api/provisioning"
    )
    os.environ["REDTEAM_API_URL"] = (
        f"https://app.{active_profile_domain}/proxy/{lab_id}/api/redteam"
    )


def lab_unset_lab_handler(args: Any) -> None:
    del os.environ["PROVISIONING_API_URL"]
    del os.environ["REDTEAM_API_URL"]


def add_lab_parser(root_parser: argparse.ArgumentParser, subparsers: Any) -> None:
    # Subparser lab
    parser_lab = subparsers.add_parser(
        "lab",
        help="Scenario API related commands (lab)",
        formatter_class=root_parser.formatter_class,
    )
    parser_lab.set_defaults(set_lab=lab_set_lab_handler)
    parser_lab.set_defaults(unset_lab=lab_unset_lab_handler)
    parser_lab.add_argument("lab_id", type=str, help="The lab id")
    subparsers_lab = parser_lab.add_subparsers()

    # 'lab_info' command
    parser_lab_info = subparsers_lab.add_parser(
        "info",
        help="Get information about a lab",
        formatter_class=root_parser.formatter_class,
    )
    parser_lab_info.set_defaults(func=lab_info_handler)
    parser_lab_info.add_argument(
        "--json", help="Return JSON result.", action="store_true"
    )

    # 'lab_api' command
    parser_lab_api = subparsers_lab.add_parser(
        "api",
        help="Get API URLs to directly access the lab",
        formatter_class=root_parser.formatter_class,
    )
    parser_lab_api.set_defaults(func=lab_api_handler)
    parser_lab_api.add_argument(
        "--json", help="Return JSON result.", action="store_true"
    )

    # 'lab_stop' command
    parser_lab_stop = subparsers_lab.add_parser(
        "stop", help="Stop a specific lab", formatter_class=root_parser.formatter_class
    )
    parser_lab_stop.set_defaults(func=lab_stop_handler)

    # 'lab_delete_lab' command
    parser_lab_delete_lab = subparsers_lab.add_parser(
        "delete",
        help="Delete lab from its lab id",
        formatter_class=root_parser.formatter_class,
    )
    parser_lab_delete_lab.set_defaults(func=lab_delete_lab_handler)

    # 'lab_resume' command
    parser_lab_resume = subparsers_lab.add_parser(
        "resume",
        help="Resume a specific lab",
        formatter_class=root_parser.formatter_class,
    )
    parser_lab_resume.set_defaults(func=lab_resume_handler)

    # 'lab_topology' command
    parser_lab_topology = subparsers_lab.add_parser(
        "topology",
        help="Get scenario topology on current lab",
        formatter_class=root_parser.formatter_class,
    )
    parser_lab_topology.set_defaults(func=lab_topology_handler)

    # 'lab_nodes' command
    parser_lab_nodes = subparsers_lab.add_parser(
        "nodes",
        help="Get scenario nodes on current lab",
        formatter_class=root_parser.formatter_class,
    )
    parser_lab_nodes.set_defaults(func=lab_nodes_handler)

    # 'lab_assets' command
    parser_lab_assets = subparsers_lab.add_parser(
        "assets",
        help="Get scenario assets on current lab",
        formatter_class=root_parser.formatter_class,
    )
    parser_lab_assets.set_defaults(func=lab_assets_handler)

    # 'lab_attack_report' command
    parser_lab_attack_report = subparsers_lab.add_parser(
        "attack-report",
        help="Get scenario attack report on current lab",
        formatter_class=root_parser.formatter_class,
    )
    parser_lab_attack_report.set_defaults(func=lab_attack_report_handler)

    # 'lab_attack_infras' command
    parser_lab_attack_infras = subparsers_lab.add_parser(
        "attack-infras",
        help="Get scenario attack infras on current lab",
        formatter_class=root_parser.formatter_class,
    )
    parser_lab_attack_infras.set_defaults(func=lab_attack_infras_handler)

    # 'lab_attack_sessions' command
    parser_lab_attack_sessions = subparsers_lab.add_parser(
        "attack-sessions",
        help="Get scenario attack sessions on current lab",
        formatter_class=root_parser.formatter_class,
    )
    parser_lab_attack_sessions.set_defaults(func=lab_attack_sessions_handler)

    # 'lab_attack_knowledge' command
    parser_lab_attack_knowledge = subparsers_lab.add_parser(
        "attack-knowledge",
        help="Get scenario attack knowledge on current lab",
        formatter_class=root_parser.formatter_class,
    )
    parser_lab_attack_knowledge.set_defaults(func=lab_attack_knowledge_handler)

    # 'lab_notifications' command
    parser_lab_notifications = subparsers_lab.add_parser(
        "notifications",
        help="Get scenario notifications on current lab",
        formatter_class=root_parser.formatter_class,
    )
    parser_lab_notifications.set_defaults(func=lab_notifications_handler)

    # 'lab_scenario_run_config' command
    parser_lab_scenario_run_config = subparsers_lab.add_parser(
        "scenario-run-config",
        help="Get scenario run config on current lab",
        formatter_class=root_parser.formatter_class,
    )
    parser_lab_scenario_run_config.set_defaults(func=lab_scenario_run_config_handler)

    parser_lab.set_defaults(func=lambda _: parser_lab.print_help())

    # -------------------
    # --- Redteam actions on labs
    # -------------------

    add_redteam_parser(root_parser=root_parser, subparsers=subparsers_lab)

    # -------------------
    # --- Provisioning actions on labs
    # -------------------

    add_provisioning_parser(root_parser=root_parser, subparsers=subparsers_lab)
