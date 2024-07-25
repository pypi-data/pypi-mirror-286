# -*- coding: utf-8 -*-
#
# Copyright (c) 2016-2021 AMOSSYS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
import glob
import json
import os
import pprint
import shutil
import tempfile
import time
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from urllib.parse import urlencode

import requests
from colorama import Fore
from mantis_scenario_model.notification_model import Notification
from mantis_scenario_model.notification_model import NotificationStage
from mantis_scenario_model.scenario_model import ScenarioExecutionStopped
from mantis_scenario_model.scenario_run_config_model import PositionStep
from jinja2 import Template

from cr_api_client.config import cr_api_client_config
from cr_api_client.logger import logger


# Module variables
attack_list = {}
cbk_attack_event = None
cbk_check_stopped = None
cbk_scenario_pause = None

# -------------------------------------------------------------------------- #
# Internal helpers
# -------------------------------------------------------------------------- #


def _get(route: str, **kwargs: str) -> requests.Response:
    return requests.get(
        f"{cr_api_client_config.redteam_api_url}{route}",
        verify=cr_api_client_config.cacert,
        cert=(cr_api_client_config.cert, cr_api_client_config.key),
        timeout=60,
        **kwargs,
    )


def _post(route: str, **kwargs: str) -> requests.Response:
    return requests.post(
        f"{cr_api_client_config.redteam_api_url}{route}",
        verify=cr_api_client_config.cacert,
        cert=(cr_api_client_config.cert, cr_api_client_config.key),
        timeout=60,
        **kwargs,
    )


def _put(route: str, **kwargs: str) -> requests.Response:
    return requests.put(
        f"{cr_api_client_config.redteam_api_url}{route}",
        verify=cr_api_client_config.cacert,
        cert=(cr_api_client_config.cert, cr_api_client_config.key),
        timeout=60,
        **kwargs,
    )


def _delete(route: str, **kwargs: str) -> requests.Response:
    return requests.delete(
        f"{cr_api_client_config.redteam_api_url}{route}",
        verify=cr_api_client_config.cacert,
        cert=(cr_api_client_config.cert, cr_api_client_config.key),
        timeout=120,
        **kwargs,
    )


def _handle_error(result: requests.Response, context_error_msg: str) -> None:
    if result.headers.get("content-type") == "application/json":
        error_msg = str(result.json())  # ["message"]
    else:
        error_msg = result.text

    raise Exception(
        f"{context_error_msg}. \n"
        f"Status code: '{result.status_code}'.\n"
        f"Error message: '{error_msg}'."
    )


# -------------------------------------------------------------------------- #
# Redteam API
# -------------------------------------------------------------------------- #


def get_version() -> str:
    """Return Redteam API version."""
    result = _get("/version")

    if result.status_code != 200:
        _handle_error(result, "Cannot retrieve Redteam API version")

    return result.json()


def reset_redteam() -> None:
    """Reset redteam platform (init knowledge_database and delete all workers).

    :return: None

    >>> from cr_api_client import redteam_api
    >>> redteam_api.reset_redteam()  # doctest: +SKIP

    """
    result = _delete("/platform")
    result.raise_for_status()


def logs() -> Dict:
    """Get redteam API logs.

    :return: str

    >>> from cr_api_client import redteam_api
    >>> redteam_api.reset_redteam()  # doctest: +SKIP
    >>> redteam_api.logs()  # doctest: +SKIP
    {}

    """
    url = "/logs"

    result = _get(url, headers={}, data={})

    if result.status_code != 200:
        _handle_error(result, "Cannot retrieve logs from redteam API")

    return result.json()


def attack_logs(id_attack: str) -> Dict:
    """Get docker logs for a specific attack.

    :param id_attack: The attack identifier.
    :type id_attack: :class:`int`

    :return: Logs of attack.
    :rtype: :class:`str`

    >>> from cr_api_client import redteam_api
    >>> redteam_api.reset_redteam()  # doctest: +SKIP
    >>> redteam_api.attack_logs(id_attack=1)  # doctest: +SKIP
    {}

    """
    url = "/logs/" + str(id_attack)

    result = _get(url, headers={}, data={})

    if result.status_code != 200:
        _handle_error(result, "Cannot retrieve logs from redteam API")

    return result.json()


def list_tactics() -> List[dict]:
    """List all available tactics (based on MITRE ATT&CK).

    :return: Available tactics in JSON format.
    :rtype: :class:`List`

    >>> from cr_api_client import redteam_api
    >>> redteam_api.reset_redteam()  # doctest: +SKIP
    >>> redteam_api.list_tactics()  # doctest: +SKIP
    [{'id': 'TA0001', 'name': 'Initial Access'}, {'id': 'TA0002', 'name': 'Execution'}, {'id': 'TA0003', 'name': 'Persistence'}, {'id': 'TA0004', 'name': 'Privilege Escalation'}, {'id': 'TA0005', 'name': 'Defense Evasion'}, {'id': 'TA0006', 'name': 'Credential Access'}, {'id': 'TA0007', 'name': 'Discovery'}, {'id': 'TA0008', 'name': 'Lateral Movement'}, {'id': 'TA0009', 'name': 'Collection'}, {'id': 'TA0010', 'name': 'Exfiltration'}, {'id': 'TA0011', 'name': 'Command and Control'}, {'id': 'TA0040', 'name': 'Impact'}, {'id': 'TA0042', 'name': 'Resource Development'}, {'id': 'TA0043', 'name': 'Reconnaissance'}]

    """
    url = "/tactic"

    result = _get(url, headers={}, data={})

    if result.status_code != 200:
        _handle_error(result, "Cannot retrieve available tactics from redteam API")

    return result.json()


def list_workers() -> List[dict]:
    """List all available workers.

    :return: Available workers in JSON format.
    :rtype: :class:`List`

    >>> from cr_api_client import redteam_api
    >>> redteam_api.reset_redteam()  # doctest: +SKIP
    >>> redteam_api.list_workers()  # doctest: +SKIP
    [{...}]

    """
    url = "/worker"

    result = _get(url, headers={}, data={})

    if result.status_code != 200:
        _handle_error(result, "Cannot retrieve available workers from redteam API")

    return result.json()


def worker_infos(id_worker: str) -> dict:
    """Retrieve worker info from its ID.

    :return: Worker info in JSON format.
    :rtype: :class:`List`

    >>> from cr_api_client import redteam_api
    >>> redteam_api.reset_redteam()  # doctest: +SKIP
    >>> redteam_api.worker_infos("1021_006_002")  # doctest: +SKIP
    {'id': '1021_006_002', 'name': 'winrm_session', ...}

    """
    url = f"/worker/{id_worker}"

    result = _get(url, headers={}, data={})

    if result.status_code != 200:
        _handle_error(result, "Cannot retrieve worker info from redteam API")

    return result.json()


def list_attacks(status: str = None) -> List[dict]:
    """List all attacks available and done.

    :param status: The status (success, failed, error, running, runnable) to filter.
    :type status: :class:`str`

    :return: List all attacks in JSON format.
    :rtype: :class:`List`

    >>> from cr_api_client import redteam_api
    >>> redteam_api.reset_redteam()  # doctest: +SKIP
    >>> redteam_api.list_attacks(status="success")  # doctest: +SKIP
    []

    """
    url = "/attack"

    if status:
        url = url + "?status=" + status
    result = _get(url, headers={}, data={})

    if result.status_code != 200:
        _handle_error(result, "Cannot retrieve available attacks from redteam API")

    return result.json()


def attack_infos(id_attack: str) -> Dict:
    """Return all data for an attack.

    :param id_attack: The attack identifier.
    :type id_attack: :class:`int`

    :return: Attack data.
    :rtype: :class:`Dict`

    >>> from cr_api_client import redteam_api
    >>> redteam_api.reset_redteam()  # doctest: +SKIP
    >>> redteam_api.attack_infos(id_attack=1)  # doctest: +SKIP
    ('runnable', None)

    """
    url = "/attack/" + str(id_attack)

    result = _get(url, headers={}, data={})
    if result.status_code != 200:
        _handle_error(result, "Cannot retrieve attack from redteam API")
    res_json = result.json()

    for key, value in res_json.items():
        if isinstance(value, str):
            try:
                res_json[key] = json.loads(value)
            except json.JSONDecodeError:
                pass
    return res_json


def __waiting_attack(
    id_attack: str,
    name: str,
    waiting_worker: bool = True,
    debug: bool = False,
    allow_to_failed: bool = False,
) -> Tuple[str, Dict]:
    """
    Waiting for attack status (waiting, success or failed).

    :param id_attack: The attack identifier.
    :type id_attack: :class:`int`
    :param attack_name: The worker name for this attack.
    :type attack_name: :class:`str`
    :param waiting_worker: Wait attack status become "success" or "failed".
    :type waiting_worker: :class:`bool`, optional

    :return: The attack step report.
    :rtype: :class:`Dict`

    """
    url = "/attack/" + str(id_attack)

    result = _get(url, headers={}, data={})

    if result.status_code != 200:
        _handle_error(result, "Cannot retrieve attack information from redteam API")

    status = result.json().get("status", None)
    cpt_max = 150
    cpt = 0
    while status not in ["success", "failed", "error"]:  # not finished

        if cbk_check_stopped is not None:
            if cbk_check_stopped() is True:
                logger.info("   [+]    Current process was asked to stop")
                raise ScenarioExecutionStopped

        time.sleep(1)
        cpt = cpt + 1
        result = _get(url, headers={}, data={})

        if result.status_code != 200:
            _handle_error(result, "Cannot retrieve attack information from redteam API")

        status = result.json().get("status", None)
        if status == "waiting":
            logger.info(f"[+] ({id_attack}) Attack {name} is waiting.")
            if not waiting_worker:
                return
        if cpt == cpt_max:
            status = "error"
            _handle_error(result, f"Attack {name} error : TIMEOUT")
        time.sleep(1)

    if status == "success":
        color = Fore.GREEN
    elif status == "failed":
        color = Fore.YELLOW
        if not allow_to_failed:
            output = result.json().get("output", "")
            _handle_error(result, f"Attack {name} failed : {output}")
    elif status == "error":
        color = Fore.RED
        output = result.json().get("output", "")
        _handle_error(result, f"Attack {name} error : {output}")

    logger.info(
        f"[+] {Fore.BLUE}({id_attack}) Attack {name}{Fore.RESET} : {color}{status}{Fore.RESET}"
    )

    # Retrieve attack step report
    attack_report = {}
    scenario_report = scenario_result()
    for current_attack_report in scenario_report:
        if str(current_attack_report["id"]) == str(id_attack):
            attack_report = current_attack_report
            break

    # Retrieve debug value from var env
    debug_env = os.getenv("CR_DEBUG", "0")

    # Debug value can either be set from var env or from function parameter
    if debug or debug_env == "1":
        pp = pprint.PrettyPrinter(width=160)

        logger.info("[+] Attack report")
        pp.pprint(attack_report)

        # Retrieve worker logs
        logger.info("[+] Attack worker logs")
        redteam_logs = logs()

        if str(id_attack) in redteam_logs:
            for log in redteam_logs[str(id_attack)]:
                print(log)

    return attack_report


def execute_attack_by_id(
    id_attack: int,
    name: str,
    waiting_worker: bool = True,
    options: Dict = {},
    debug: bool = False,
    allow_to_failed: bool = False,
    title: str = "",
) -> Optional[str]:
    """
    Start attack by id_attack.

    :param id_attack: The attack identifier.
    :type id_attack: :class:`int`
    :param attack_name: The worker name for this attack.
    :type attack_name: :class:`str`
    :param waiting_worker: Wait attack status become "success" or "failed".
    :type waiting_worker: :class:`bool`, optional

    :return: The ID of attack.
    :rtype: :class:`str`

    """

    if cbk_scenario_pause is not None:
        cbk_scenario_pause(name, PositionStep.before, title)

    if cbk_attack_event is not None:
        cbk_attack_event(
            Notification(
                event_data=f"Begin attack '{title}'", stage=NotificationStage.redteam
            )
        )

    url = "/attack/" + str(id_attack) + "/play"
    if options:
        url = url + "?" + urlencode(options)
    payload = {}
    headers = {}
    result = _get(url, headers=headers, data=payload)

    if result.status_code != 200:
        _handle_error(result, "Cannot start attack from redteam API")

    result = result.json()
    idAttack = result.get("idAttack", None)
    logger.info(f"[+] {Fore.BLUE}({idAttack}) Attack {name}{Fore.RESET} : started")
    logger.info(f"[+]     Values : {Fore.YELLOW}{result['values']}{Fore.RESET}")
    if idAttack is not None:
        result = __waiting_attack(
            idAttack, name, waiting_worker, debug=debug, allow_to_failed=allow_to_failed
        )
        if waiting_worker:
            attack_report = result

            if cbk_attack_event is not None:
                output = f"Finished attack '{title}'"

                # Add some attack context to the callback
                if "target_nodes" in attack_report:
                    for target_node in attack_report["target_nodes"]:
                        if "node_type" in target_node:
                            if target_node["node_type"] == "ATTACK_SESSION":
                                output += f" on {target_node['node_info']['ip']} (session={target_node['node_info']['type_session']}, user={target_node['node_info']['username']}, privilege={target_node['node_info']['privilege_level']})"

                            if "attack_process_graph" in target_node:
                                for process in target_node["attack_process_graph"]:
                                    if "sh" in process:
                                        output += f" - command: {process['sh']['decoded_command']}"
                                    elif "powershell" in process:
                                        output += f" - command: {process['powershell']['decoded_command']}"

                cbk_attack_event(
                    Notification(event_data=output, stage=NotificationStage.redteam)
                )
        else:
            if cbk_attack_event is not None:
                cbk_attack_event(
                    Notification(
                        event_data=f"Attack '{title}' is in waiting mode",
                        stage=NotificationStage.redteam,
                    )
                )

    return idAttack


def execute_attack(
    attack_name: str,
    retries: int = 3,
    attack_session_identifier: Optional[str] = None,
    attack_values_dict: Optional[Dict[str, Any]] = None,
    attack_values_callback: Optional[Callable[[Dict[str, Any]], bool]] = None,
    waiting_worker: bool = True,
    options: Dict = {},
    allow_to_failed: bool = False,
) -> Optional[str]:
    """
    Execute attack by name, and filter by ID session or attack values.

    :param attack_name: The worker name for this attack.
    :param retries: Number of retries if attack not found.
    :param attack_session_identifier: (Optional) The ID of the attack session to use for this attack
    :param attack_values_dict: (Optional) Other key/values searched in the attack values
    :param attack_values_callback: (Optional) Callback to select an attack, based on its attack
        values, in a custom way
    :param waiting_worker: Wait attack status become "success" or "failed".
    :param options: Dict of options to worker

    :return: The ID of attack.
    """

    attack = None
    for _ in range(retries):
        attack = get_attack_by_values(
            attack_name,
            attack_session_identifier=attack_session_identifier,
            attack_values_dict=attack_values_dict,
            attack_values_callback=attack_values_callback,
        )
        if attack:
            break
        else:
            time.sleep(1)

    if not attack:
        message = f"Attack '{attack_name}' was not found after {retries} retries"

        if attack_session_identifier:
            message += f", for attack session id {attack_session_identifier}."

        if attack_values_dict and not attack_values_callback:
            message += f", for attack values {attack_values_dict}."
        elif not attack_values_dict and attack_values_callback:
            message += ", for attack values selected by a callback."
        elif attack_values_dict and attack_values_callback:
            message += f", for attack values {attack_values_dict} and further selected by a callback."

        raise Exception(message)

    idAttack = execute_attack_by_id(
        attack["idAttack"],
        attack["worker"]["name"],
        waiting_worker=waiting_worker,
        options=options,
        allow_to_failed=allow_to_failed,
        title=attack["worker"]["title"],
    )
    if cbk_scenario_pause is not None:
        cbk_scenario_pause(
            attack["worker"]["name"], PositionStep.after, attack["worker"]["title"]
        )
    return idAttack


def get_attack_by_values(
    attack_name: str,
    attack_session_identifier: Optional[str] = None,
    attack_values_dict: Optional[Dict[str, Any]] = None,
    attack_values_callback: Optional[Callable[[Dict[str, Any]], bool]] = None,
) -> Dict[str, Any]:
    """
    Helper function to find an attack for a specific attack session or for specific attack values

    Allows to search for an available an attack based on its name, and several optional criteria.
    The selection can be done based one:

    * the ID of the attack session to use
    * specific, exact keys/values in the attack values
    * a custom callback, for more complex selection

    The three selection methods can be combined. If two or all three parameters are used
    (`attack_session_identifier`, `attack_values_dict`, `attack_values_callback`), an attack is
    searched that matches all three parameters.

    Example:
    >>> from cr_api_client import redteam_api
    >>> attack_session_id = "d5f7a6a3-54c7-4666-9e9d-31cbc404c21b"
    >>> attack_values_dict = {"target_ip": "1.2.3.4", "param1": 42}
    >>> attack_values_callback = lambda values: "param2" in values and "substring" in values["param2"]
    >>> redteam_api.get_attack_by_values("my_worker_name", attack_session_id, attack_values_dict, attack_values_callback)  # doctest: +SKIP
    {'idAttack': 23, 'worker': {'id': '1487_000_001', 'name': 'my_worker_name', 'description':
    'XXX', 'cve': [],'stability': 'CRASH_SAFE', 'reliability': 'UNIQUE', 'side_effect':
    'NETWORK_CONNECTION', 'killchain_step': 'EXECUTION', 'repeatable': False, 'mitre_data':
    {'technique': {'id': 'T1487', 'name': 'Techname'}, 'subtechnique': {}, 'tactics': [{'id':
    'TA0002', 'name': 'Execution'}]}}, 'status': 'runnable', 'created_date':
    '2023-03-09T17:12:00+01:00', 'started_date': '', 'last_update': '', 'commands': None, 'values':
    '{"target_ip": "1.2.3.4", "param3": "value3", "param2: "this string contains a substring, it
    does, "param1": 42, attack_session_id": "d5f7a6a3-54c7-4666-9e9d-31cbc404c21b"}', 'output': None, 'source': None, 'infrastructure': '{"ip_api_public":
    "91.160.8.7", "domain_name_public": "dpcbwesnmecppni.co.uk", "ip_api_private": "192.168.66.2",
    "type": "C&C_HTTP", "webserver": "91.160.8.8"}', 'docker_id': "f44a56c89e"}

    :param attack_name: The worker name for this attack.
    :type attack_name: :class:`str`
    :param attack_session_identifier: (Optional) The ID of the attack session to use for this attack
    :type attack_session_identifier: class:`str`
    :param attack_values_dict: (Optional) Other key/values searched in the attack values
    :type attack_values_dict: class:`Dict[str, Any]`
    :param attack_values_callback: (Optional) Callback to select an attack, based on its attack
        values, in a custom way
    :type attack_values_callback: class:`Callable[[Dict[str, Any]], bool]`

    :return: The dict of the attack (with keys idAttack, worker, status, values, etc.)
    :rtype: :class:`Dict[str, Any]`
    """

    # The constraint on attack session id is actually a constraint expressed by the dict
    # attack_values_dict
    if attack_session_identifier:
        if attack_values_dict is None:
            attack_values_dict = {}
        attack_values_dict["attack_session_id"] = attack_session_identifier

    for attack in list_attacks():
        if (
            attack
            and attack["values"] != '"None"'
            and attack["worker"]["name"] == attack_name
        ):
            attack_values = json.loads(attack["values"])
            attack_values_match = True

            # Check constraints on the value
            # By dict (exact values)
            if attack_values_dict:
                for k, v in attack_values_dict.items():
                    if k not in attack_values or attack_values[k] != v:
                        attack_values_match = False

            # By callback
            if attack_values_callback:
                attack_values_match = attack_values_match and attack_values_callback(
                    attack_values
                )

            # If all constraints are respected, the attack is the right one
            if attack_values_match:
                return attack


def init_knowledge(topic_name: str, data: List[Any]) -> bool:
    """
    Insert data in knowledge database.

    :return: boolean

    >>> from cr_api_client import redteam_api
    >>> from mantis_redteam_model.topic_model import Host, HostInfos
    >>> redteam_api.reset_redteam()  # doctest: +SKIP
    >>> host = HostInfos(hostname="WIN", netbios_name="WIN_X")
    >>> host_config = Host(host_ip="x.x.x.x", host=host)
    >>> redteam_api.init_knowledge("host", [host_config])  # doctest: +SKIP
    True

    """
    json_data = {"topic_name": topic_name, "topic_data": [d.to_dict() for d in data]}

    url = "/knowledge"
    headers = {"Content-type": "application/json"}
    result = _post(url, headers=headers, data=json.dumps(json_data))

    if result.status_code != 200:
        _handle_error(result, "Cannot initialize knowledge database from redteam API")
    else:
        return True


def scenario_result() -> str:
    """
    Generate json report about all attack actions.

    :return: List all attacks done and runnning.

    >>> from cr_api_client import redteam_api
    >>> redteam_api.reset_redteam()  # doctest: +SKIP
    >>> redteam_api.scenario_result()  # doctest: +SKIP
    []

    """

    url = "/report"

    result = _get(url, headers={}, data={})

    if result.status_code != 200:
        _handle_error(result, "Cannot get scenario result from redteam API")

    return result.json()


def attack_knowledge() -> str:
    """
    Get the attack knowledge (attack hosts and sessions).

    :return: Attack hosts and sessions.

    >>> from cr_api_client import redteam_api
    >>> redteam_api.reset_redteam()  # doctest: +SKIP
    >>> redteam_api.attack_knowledge()  # doctest: +SKIP
    {'hosts': [], 'network_interfaces': [], 'services': [], 'softwares': [], 'credentials': [], 'payloads': [], 'files': [], 'ad_groups': []}

    """

    url = "/attack_knowledge"

    result = _get(url, headers={}, data={})
    if result.status_code != 200:
        _handle_error(result, "Cannot get attack knowledge result from redteam API")

    try:
        return result.json()
    except Exception:
        raise Exception(
            "Cannot get attack knowledge result from redteam API: invalid JSON received from /attack_knowledge endpoint"
        )


def attack_sessions() -> List:
    """
    Show available redteam attack sessions.

    :return: Attack sessions.

    >>> from cr_api_client import redteam_api
    >>> redteam_api.reset_redteam()  # doctest: +SKIP
    >>> redteam_api.attack_sessions()  # doctest: +SKIP
    []

    """

    url = "/attack_sessions"

    result = _get(url, headers={}, data={})

    if result.status_code != 200:
        _handle_error(result, "Cannot get attack knowledge result from redteam API")

    try:
        knowledge = result.json()
    except Exception:
        raise Exception(
            "Cannot get attack knowledge result from redteam API: invalid JSON received from /attack_session endpoint"
        )

    if "attack_sessions" in knowledge:
        attack_sessions = knowledge["attack_sessions"]
    else:
        raise Exception(
            "Cannot get attack knowledge result from redteam API: invalid JSON received from /attack_session endpoint"
        )

    return attack_sessions


def execute_command(
    command: str, attack_session_identifier: str, background: bool = False
) -> Tuple[bool, str]:
    """
    Execute custom command on attack session.

    :return: boolean
    """

    if background:
        command = f"""Invoke-WmiMethod -path win32_process -name create -argumentlist ("{command}")"""

    json_data = {"command": command, "identifier": attack_session_identifier}

    url = "/command"
    headers = {"Content-type": "application/json"}
    result = _post(url, headers=headers, data=json.dumps(json_data))

    if result.status_code != 200:
        _handle_error(result, "Cannot execute custom command from Redteam API")
    else:
        return True, result.json()


def get_command(command_id: str):
    """
    Get information about a custom command

    :return: Command
    """

    url = "/command/" + str(command_id)

    payload = {}
    headers = {}
    result = _get(url, headers=headers, data=payload)

    if result.status_code != 200:
        _handle_error(result, "Cannot retrieve command information from redteam API")

    result = result.json()

    return result


def get_commands():
    """
    List all executed custom commands.

    :return: List
    """

    url = "/command"

    payload = {}
    headers = {}
    result = _get(url, headers=headers, data=payload)

    if result.status_code != 200:
        _handle_error(result, "Cannot retrieve commands list from redteam API")

    result = result.json()

    return result


def upload_file(filepath: str, attack_session_identifier: str) -> bool:
    """
    Upload a file on target by attack session.


    :return: boolean
    """

    if not os.path.isfile(filepath):
        raise Exception(f"File {filepath} doesn't exist \n")

    json_data = {"upload_file": open(filepath, "rb")}

    url = "/upload?identifier=" + attack_session_identifier
    result = _post(url, files=json_data)

    if result.status_code != 200:
        _handle_error(
            result, f"Cannot upload file in attack session {attack_session_identifier}"
        )
    else:
        return True


def infrastructures() -> List:
    """
    Show redteam attack infrastructures.

    :return: Attack infractructures.

    >>> from cr_api_client import redteam_api
    >>> redteam_api.reset_redteam()  # doctest: +SKIP
    >>> redteam_api.infrastructures()  # doctest: +SKIP
    []

    """

    url = "/attack_infrastructures"

    result = _get(url, headers={}, data={})

    if result.status_code != 200:
        _handle_error(result, "Cannot get attack knowledge result from redteam API")

    try:
        knowledge = result.json()
    except Exception:
        raise Exception(
            "Cannot get attack infrastructure result from redteam API: invalid JSON received from /attack_infrastructures endpoint"
        )

    if "attack_infrastructures" in knowledge:
        infrastructures = knowledge["attack_infrastructures"]
    else:
        raise Exception(
            "Cannot get attack infrastructure result from redteam API: invalid JSON received from /attack_infrastructures endpoint"
        )

    return infrastructures


# -------------------------------------------------------------------------- #
# Utils
# -------------------------------------------------------------------------- #


def copy_dir_and_replace_jinja(
    path: str, mapping: Dict[str, str], extensions: List[str]
) -> tempfile.TemporaryDirectory:
    """Copy path directory in a temp directory and replace jinja values
    in each file with given extension.

    """
    temp_path = tempfile.TemporaryDirectory()

    shutil.copytree(path, temp_path.name, dirs_exist_ok=True)
    for extension in extensions:
        for found_file in glob.glob(f"{temp_path.name}/*.{extension}"):
            template = Template(open(found_file).read())
            new_data = template.render(mapping)

            fd = open(found_file, "w")
            fd.write(new_data)
            fd.close()

    return temp_path
