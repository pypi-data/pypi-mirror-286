#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from typing import Any
from typing import Dict
from typing import List

import requests
from mantis_scenario_model.basebox_model import Basebox
from mantis_scenario_model.scenario_model import Scenario
from mantis_scenario_model.scenario_run_config_model import ScenarioRunConfig
from mantis_scenario_model.topology_model import Topology
from mantis_scenario_model.unit_attack_model import UnitAttack
from pydantic import parse_obj_as

from mantis_api_client.config import mantis_api_client_config
from mantis_api_client.oidc import authorize

# -------------------------------------------------------------------------- #
# Internal helpers
# -------------------------------------------------------------------------- #


def _get(route: str, **kwargs: Any) -> requests.Response:
    return requests.get(
        f"{mantis_api_client_config.scenario_api_url}{route}",
        verify=mantis_api_client_config.cacert,
        cert=(mantis_api_client_config.cert, mantis_api_client_config.key),
        timeout=30,
        **kwargs,
    )


def _post(route: str, **kwargs: Any) -> requests.Response:
    return requests.post(
        f"{mantis_api_client_config.scenario_api_url}{route}",
        verify=mantis_api_client_config.cacert,
        cert=(mantis_api_client_config.cert, mantis_api_client_config.key),
        timeout=30,
        **kwargs,
    )


def _put(route: str, **kwargs: Any) -> requests.Response:
    return requests.put(
        f"{mantis_api_client_config.scenario_api_url}{route}",
        verify=mantis_api_client_config.cacert,
        cert=(mantis_api_client_config.cert, mantis_api_client_config.key),
        timeout=30,
        **kwargs,
    )


def _delete(route: str, **kwargs: Any) -> requests.Response:
    return requests.delete(
        f"{mantis_api_client_config.scenario_api_url}{route}",
        verify=mantis_api_client_config.cacert,
        cert=(mantis_api_client_config.cert, mantis_api_client_config.key),
        timeout=30,
        **kwargs,
    )


def _handle_error(
    result: requests.Response, context_error_msg: str
) -> requests.Response:
    error_msg = ""
    if result.headers.get("content-type") == "application/json":
        error_data = result.json()
        for k in ("message", "detail"):
            if k in error_data:
                error_msg = error_data[k]
                break
    if not error_msg:
        error_msg = result.text

    raise Exception(
        f"{context_error_msg}. "
        f"Status code: '{result.status_code}'.\n"
        f"Error message: '{error_msg}'."
    )


# -------------------------------------------------------------------------- #
# Internal helpers
# -------------------------------------------------------------------------- #


def get_version() -> str:
    """
    Return publish API version.

    :return: The version number is a string
    """
    result = _get("/version")

    if result.status_code != 200:
        _handle_error(result, "Cannot retrieve scenario API version")

    return result.json()


# -------------------------------------------------------------------------- #
# Scenario API
# -------------------------------------------------------------------------- #


def fetch_attacks() -> Any:
    """
    List all available unit attacks

    :return: the list of unit attacks
    """
    result = authorize(_get)("/unit_attack")

    if result.status_code != 200:
        _handle_error(result, "Cannot retrieve unit attacks from scenario API")
    else:
        attacks_data = result.json()
        attacks = parse_obj_as(List[UnitAttack], attacks_data)

    return attacks


def fetch_attack_by_name(attack_name: str) -> Any:
    """
    Get the full JSON manifest of a specific unit attack

    :param attack_name: the name of the unit attack to fetch

    :return: the JSON of unit attacks
    """
    result = authorize(_get)(f"/unit_attack/{attack_name}")

    if result.status_code != 200:
        _handle_error(
            result,
            f"Cannot retrieve unit attack '{attack_name}' from frontend publish API",
        )
    else:
        attack_data = result.json()
        attack = UnitAttack(**attack_data)

    return attack


def fetch_scenarios() -> List[Scenario]:
    """
    List all available scenarios

    :return: the list of scenarios
    """
    result = authorize(_get)("/scenario")

    if result.status_code != 200:
        _handle_error(result, "Cannot retrieve scenarios from scenario API")
    else:
        scenarios_data = result.json()
        scenarios = parse_obj_as(List[Scenario], scenarios_data)

    return scenarios


def fetch_scenario_by_name(scenario_id: str) -> Scenario:
    """
    Get the full JSON manifest of a specific scenario.

    :param scenario_id: id of the scenario to fetch

    :return: the JSON of the scenario
    """
    result = authorize(_get)(f"/scenario/{scenario_id}")

    if result.status_code != 200:
        _handle_error(
            result, f"Cannot retrieve scenario '{scenario_id}' from scenario API"
        )
    else:
        scenario_data = result.json()
        scenario = Scenario(**scenario_data)

    return scenario


def fetch_topologies() -> List[Topology]:
    """
    List all available topologies

    :return: the list of topologies
    """
    result = authorize(_get)("/topology")

    if result.status_code != 200:
        _handle_error(result, "Cannot retrieve topologies from scenario API")
    else:
        topologies_data = result.json()
        topologies = parse_obj_as(List[Topology], topologies_data)

    return topologies


def fetch_topology_by_name(topology_name: str) -> Topology:
    """
    Get the topology object given its name.

    :param topology_name: name of the topology

    :return: the topology object
    """
    result = authorize(_get)(f"/topology/{topology_name}")

    if result.status_code != 200:
        _handle_error(
            result, f"Cannot retrieve topology '{topology_name}' from scenario API"
        )
    else:
        topology_data = result.json()
        topology = Topology(**topology_data)

    return topology


def fetch_baseboxes() -> List[Basebox]:
    """
    List all available baseboxes

    :return: the list of baseboxes
    """
    result = authorize(_get)("/basebox")

    if result.status_code != 200:
        _handle_error(result, "Cannot retrieve baseboxes from scenario API")
    else:
        baseboxes_data = result.json()
        baseboxes = parse_obj_as(List[Basebox], baseboxes_data)

    return baseboxes


def fetch_basebox_by_id(basebox_id: str) -> Basebox:
    """
    Get the basebox object given its ID.

    :param basebox_id: name of the basebox

    :return: the basebox object
    """
    result = authorize(_get)(f"/basebox/{basebox_id}")

    if result.status_code != 200:
        _handle_error(
            result, f"Cannot retrieve basebox '{basebox_id}' from scenario API"
        )
    else:
        basebox_data = result.json()
        basebox = Basebox(**basebox_data)

    return basebox


def get_log_collectors() -> dict:
    """
    Retrieve log collectors configuration information.
    """

    result = authorize(_get)("/log_collector")

    if result.status_code != 200:
        _handle_error(
            result,
            "Cannot get log collectors data from scenario API",
        )

    return result.json()


def run_topology(
    topology: Topology, scenario_run_config: ScenarioRunConfig, group_id: str
) -> str:
    """
    Run the given topology.

    :param topology: the topology to run

    :return: a lab id
    """

    # Convert model into dict
    scenario_run_config_dict = json.loads(scenario_run_config.json())

    # API call
    result = authorize(_post)(
        f"/topology/{topology.name}/run",
        params={"group_id": group_id},
        json={"scenario_run_config": scenario_run_config_dict},
    )

    if result.status_code != 200:
        _handle_error(
            result, f"Cannot run topology '{topology.name}' from scenario API"
        )

    return result.json()


def run_basebox(
    basebox_id: str, scenario_run_config: ScenarioRunConfig, group_id: str
) -> str:
    """
    Run the given basebox.

    :param basebox_id: the basebox to run

    :return: a lab id
    """

    # Convert model into dict
    scenario_run_config_dict = json.loads(scenario_run_config.json())

    # API call
    result = authorize(_post)(
        f"/basebox/{basebox_id}/run",
        params={"group_id": group_id},
        json={"scenario_run_config": scenario_run_config_dict},
    )

    if result.status_code != 200:
        _handle_error(result, f"Cannot run basebox '{basebox_id}' from scenario API")

    return result.json()


def run_scenario(
    scenario: Scenario,
    scenario_run_config: ScenarioRunConfig,
    group_id: str,
    scenario_config_name: str,
) -> str:
    """
    Run the given scenario.

    :param scenario: the scenario to run

    :return: a lab id
    """

    # Convert model into dict
    scenario_run_config_dict = json.loads(scenario_run_config.json())

    # API call
    result = authorize(_post)(
        f"/scenario/{scenario.name}/run",
        params={"group_id": group_id},
        json={
            "scenario_run_config": scenario_run_config_dict,
            "scenario_config_name": scenario_config_name,
        },
    )

    if result.status_code != 200:
        _handle_error(
            result, f"Cannot run scenario '{scenario.name}' from scenario API"
        )

    return result.json()


def run_attack(
    attack: UnitAttack,
    scenario_config_name: str,
    scenario_run_config: ScenarioRunConfig,
    group_id: str,
) -> str:
    """
    Run the given attack.

    :param attack: the attack to run
    :param scenario_config_name: the unit scenario to run for the current attack

    :return: a lab id
    """

    # Convert model into dict
    scenario_run_config_dict = json.loads(scenario_run_config.json())

    # API call
    result = authorize(_post)(
        f"/unit_attack/{attack.name}/run",
        params={"group_id": group_id},
        json={
            "scenario_run_config": scenario_run_config_dict,
            "scenario_config_name": scenario_config_name,
        },
    )

    if result.status_code != 200:
        _handle_error(result, f"Cannot run attack '{attack.name}' from scenario API")

    return result.json()


def fetch_labs(all_labs: bool = False) -> List:
    """
    Get list of current labs.
    If all_labs is True, retrieve also stopped labs.

    :return: a list containg the current labs.
    """
    params = {"all_labs": all_labs}
    result = authorize(_get)("/runner", params=params)

    if result.status_code != 200:
        _handle_error(result, "Cannot get lab list from scenario API")

    return result.json()


def fetch_lab(lab_id: str) -> Dict:
    """
    Get status of a lab.

    :param lab_id: the lab id

    :return: a dict containg the lab status and potential results
    """
    result = authorize(_get)(f"/runner/{lab_id}")

    if result.status_code != 200:
        _handle_error(
            result, f"Cannot get lab status from id '{lab_id}' from scenario API"
        )

    return result.json()


def stop_lab(lab_id: str) -> None:
    """
    Stop lab execution.

    :param lab_id: the lab id

    :return: a dict containg the lab status and potential results
    """
    result = authorize(_get)(f"/runner/{lab_id}/stop")

    if result.status_code != 200:
        _handle_error(
            result,
            f"Cannot stop lab execution of id '{lab_id}' from scenario API",
        )


def resume_lab(lab_id: str) -> None:
    """
    Stop lab execution.

    :param lab_id: the lab id

    :return: a dict containg the lab status and potential results
    """
    result = authorize(_get)(f"/runner/{lab_id}/resume")

    if result.status_code != 200:
        _handle_error(
            result,
            f"Cannot resume lab execution of id '{lab_id}' from scenario API",
        )


def fetch_lab_topology(lab_id: str) -> Dict:
    """
    Get scenario topology of a current lab.

    :param lab_id: the lab id

    :return: a dict containg the topology
    """
    result = authorize(_get)(f"/runner/{lab_id}/topology")

    if result.status_code != 200:
        _handle_error(
            result,
            f"Cannot get scenario topology from id '{lab_id}' from scenario API",
        )

    return result.json()


def fetch_lab_nodes(lab_id: str) -> List:
    """
    Get scenario nodes of a current lab.

    :param lab_id: the lab id

    :return: the current nodes
    """
    result = authorize(_get)(f"/runner/{lab_id}/nodes")

    if result.status_code != 200:
        _handle_error(
            result, f"Cannot get scenario nodes from id '{lab_id}' from scenario API"
        )

    return result.json()


def fetch_lab_assets(lab_id: str) -> List:
    """
    Get scenario assets of a current lab.

    :param lab_id: the lab id

    :return: the current assets
    """
    result = authorize(_get)(f"/runner/{lab_id}/assets")

    if result.status_code != 200:
        _handle_error(
            result,
            f"Cannot get scenario assets from id '{lab_id}' from scenario API",
        )

    return result.json()


def fetch_lab_attack_report(lab_id: str) -> List:
    """
    Get scenario attack report of a current lab.

    :param lab_id: the lab id

    :return: the current attack report
    """
    result = authorize(_get)(f"/runner/{lab_id}/attack_report")

    if result.status_code != 200:
        _handle_error(
            result,
            f"Cannot get scenario attack report from id '{lab_id}' from scenario API",
        )

    return result.json()


def fetch_lab_attack_infras(lab_id: str) -> List:
    """
    Get scenario attack infrastructures of a current lab.

    :param lab_id: the lab id

    :return: the current attack infrastructures
    """
    result = authorize(_get)(f"/runner/{lab_id}/attack_infras")

    if result.status_code != 200:
        _handle_error(
            result,
            f"Cannot get scenario attack infras from id '{lab_id}' from scenario API",
        )

    return result.json()


def fetch_lab_attack_sessions(lab_id: str) -> List:
    """
    Get scenario attack sessions of a current lab.

    :param lab_id: the lab id

    :return: the current attack sessions
    """
    result = authorize(_get)(f"/runner/{lab_id}/attack_sessions")

    if result.status_code != 200:
        _handle_error(
            result,
            f"Cannot get scenario attack sessions from id '{lab_id}' from scenario API",
        )

    return result.json()


def fetch_lab_attack_knowledge(lab_id: str) -> Dict:
    """
    Get scenario attack knowledge of a current lab.

    :param lab_id: the lab id

    :return: the attack knowledge
    """
    result = authorize(_get)(f"/runner/{lab_id}/attack_knowledge")

    if result.status_code != 200:
        _handle_error(
            result,
            f"Cannot get scenario attack knowledge from id '{lab_id}' from scenario API",
        )

    return result.json()


def fetch_lab_notifications(lab_id: str) -> List:
    """
    Get scenario notifications of a current lab.

    :param lab_id: the lab id

    :return: the notifications as a list of strings
    """
    result = authorize(_get)(f"/runner/{lab_id}/notifications")

    if result.status_code != 200:
        _handle_error(
            result,
            f"Cannot get scenario notifications from id '{lab_id}' from scenario API",
        )

    return result.json()


def delete_lab(lab_id: str) -> None:
    """
    Delete a lab from its ID.

    :param lab_id: the lab id
    """
    result = authorize(_delete)(f"/runner/{lab_id}")

    if result.status_code != 200:
        _handle_error(
            result,
            f"Cannot delete lab from id '{lab_id}' from scenario API",
        )


def fetch_lab_scenario_run_config(lab_id: str) -> Dict:
    """
    Get scenario run config of a current lab.

    :param lab_id: the lab id

    :return: the scenario run config
    """
    result = authorize(_get)(f"/runner/{lab_id}/scenario_run_config")

    if result.status_code != 200:
        _handle_error(
            result,
            f"Cannot get scenario run config from id '{lab_id}' from scenario API",
        )

    return result.json()
