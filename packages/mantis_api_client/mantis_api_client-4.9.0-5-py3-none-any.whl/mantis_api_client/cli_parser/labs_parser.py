# -*- coding: utf-8 -*-
import argparse
import json
import sys
from typing import Any

import mantis_api_client.scenario_api as scenario_api


#
# 'labs_handler' handler
#
def labs_handler(args: Any) -> None:
    all_labs = args.all_labs

    try:
        labs = scenario_api.fetch_labs(all_labs=all_labs)
    except Exception as e:
        print(f"Error when fetching labs: '{e}'")
        sys.exit(1)

    if args.json:
        print(json.dumps(labs))
        return

    print("[+] Available labs:")
    for lab in labs:
        print(f"  [+] \033[1mID\033[0m: {lab['runner_id']}")
        print(f"        [+] \033[1mStart time\033[0m: {lab['start_time']}")
        print(f"        [+] \033[1mStatus\033[0m: {lab['status']}")
        print(f"        [+] \033[1mType\033[0m: {lab['content_type']}")


def add_labs_parser(root_parser: argparse.ArgumentParser, subparsers: Any) -> None:
    # Subparser labs
    parser_labs = subparsers.add_parser(
        "labs", help="List current labs", formatter_class=root_parser.formatter_class
    )
    parser_labs.set_defaults(func=labs_handler)
    parser_labs.add_argument(
        "-a",
        "--all",
        action="store_true",
        dest="all_labs",
        help="Include stopped labs)",
    )
    parser_labs.add_argument("--json", help="Return JSON result.", action="store_true")
