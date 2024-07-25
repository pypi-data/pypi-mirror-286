# -*- coding: utf-8 -*-
import json
import os
import re
from datetime import datetime
from datetime import timedelta
from enum import Enum
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

from pydantic import BaseModel
from pydantic import Extra
from pydantic import validator

from .topology_model import Topology

# Load techniques and tactics
mitre_json_file_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "mitre", "mitre.json"
)
mitre_attack_data = {}
with open(mitre_json_file_path, "r") as f:
    mitre_attack_data = json.load(f)

if not mitre_attack_data:
    raise Exception("File mitre.json was not found.")


class Empty(BaseModel):
    ...

    class Config:
        extra = "forbid"


class Stability(str, Enum):
    crash_safe = "CRASH_SAFE"
    crash_service_restarts = "CRASH_SERVICE_RESTARTS"
    crash_service_down = "CRASH_SERVICE_DOWN"
    crash_os_restarts = "CRASH_OS_RESTARTS"
    crash_os_down = "CRASH_OS_DOWN"
    service_resource_loss = "SERVICE_RESOURCE_LOSS"
    os_resource_loss = "OS_RESOURCE_LOSS"


class SideEffect(str, Enum):
    network_connection = "NETWORK_CONNECTION"
    artifacts_on_disk = "ARTIFACTS_ON_DISK"
    config_changes = "CONFIG_CHANGES"
    ioc_in_logs = "IOC_IN_LOGS"
    account_lockouts = "ACCOUNT_LOCKOUTS"
    screen_effects = "SCREEN_EFFECTS"


class KillchainStep(str, Enum):
    initial_access = "INITIAL_ACCESS"
    execution = "EXECUTION"
    persistence = "PERSISTENCE"
    privilege_escalation = "PRIVILEGE_ESCALATION"
    defense_evasion = "DEFENSE_EVASION"
    credential_access = "CREDENTIAL_ACCESS"
    discovery = "DISCOVERY"
    lateral_movement = "LATERAL_MOVEMENT"
    collection = "COLLECTION"
    command_and_control = "COMMAND_AND_CONTROL"
    exfiltration = "EXFILTRATION"
    impact = "IMPACT"
    reconnaissance = "RECONNAISSANCE"
    resource_development = "RESOURCE_DEVELOPMENT"


class Topics(str, Enum):
    attack_session = "attack_session"
    host = "host"
    credential = "credential"
    file = "file"
    network = "network"
    payload = "payload"
    service = "service"
    software = "software"
    infrastructure = "infrastructure"


class AttackMode(str, Enum):
    direct = "DIRECT"
    indirect = "INDIRECT"
    offline = "OFFLINE"
    infrastructure = "INFRASTRUCTURE"


class MitreIdName(BaseModel):
    id: str
    name: str


class Implementation(BaseModel):
    id: str


class WorkerMitreData(BaseModel):
    technique: MitreIdName
    subtechnique: Union[MitreIdName, Empty]
    tactics: List[MitreIdName]
    implementation: Implementation


class TopologyUnitAttack(BaseModel):
    id: str = None  # type: ignore
    yaml: str = None  # type: ignore
    topology: Topology = None  # type: ignore


class Timestamps(BaseModel):
    start_time: datetime = None
    end_time: datetime = None
    duration: timedelta = None


class UnitAttack(BaseModel):
    name: str
    worker_id: str
    title: Optional[str] = ""
    title_fr: Optional[str] = ""
    description: str
    description_fr: str
    links: List[str] = []
    version: str
    stability: Stability
    side_effect: List[SideEffect] = []
    killchain_step: List[KillchainStep]
    repeatable: bool
    topics: List[Topics] = []
    attack_mode: AttackMode = AttackMode.indirect
    cve: List[str] = []
    mitre_data: WorkerMitreData = None  # type: ignore
    topologies: List[TopologyUnitAttack] = []
    options: List[Any] = []
    scenario_config: List[Dict] = []
    timestamps: Optional[Timestamps] = None
    creation_date: datetime
    last_update: datetime

    # Do not allow extra inputs
    class Config:
        extra = Extra.forbid
        validate_assignment = True

    @validator("worker_id")
    def valid_worker_id(cls, v: str) -> str:
        pattern = r"^\d{4}_\d{3}_\d{3}$"
        if not re.match(pattern, v):
            raise ValueError("not match")
        return v

    @validator("links")
    def set_empty_list_for_links(cls, v: Union[None, List[str]]) -> List[str]:
        if v is None:
            return []
        else:
            return v

    @validator("side_effect")
    def set_empty_list_for_side_effect(cls, v: List[str]) -> List[str]:
        return v or []

    @validator("topics")
    def set_empty_list_for_side_topics(cls, v: List[str]) -> List[str]:
        return v or []

    @validator("mitre_data", always=True)
    def set_mitre_data(cls, value: WorkerMitreData, values: Any) -> WorkerMitreData:
        if value is None:
            if "worker_id" in values:
                ids = values["worker_id"].split("_")
                technique_id = f"T{ids[0]}"
                subtechnique_id = ids[1]
                implementation_id = ids[2]

                if subtechnique_id != "000":
                    mitre_id = f"{technique_id}.{subtechnique_id}"
                else:
                    mitre_id = f"{technique_id}"

                mitre_technique = None
                mitre_subtechnique = {}
                mitre_tactic = []

                implementation = {"id": implementation_id}

                technique_name = None
                for technique in mitre_attack_data["techniques"]:
                    if technique["id"] == technique_id:
                        technique_name = technique["name"]
                        mitre_technique = MitreIdName(
                            **{"id": technique_id, "name": technique_name}
                        )
                        for subtechnique in technique["subtechniques"]:
                            if subtechnique["id"] == mitre_id:
                                mitre_subtechnique = MitreIdName(
                                    **{"id": mitre_id, "name": subtechnique["name"]}
                                )
                                break
                        for tactic in technique["tactics"]:
                            mitre_tactic.append(
                                MitreIdName(
                                    **{
                                        "id": tactic["id"],
                                        "name": tactic["name"],
                                    }
                                )
                            )
                        break

                if (
                    technique_name is None
                    or mitre_technique is None
                    or len(mitre_tactic) == 0
                    or implementation is None
                ):
                    raise Exception(f"Error getting information about {mitre_id}.")

                return WorkerMitreData(
                    **{
                        "technique": mitre_technique,
                        "subtechnique": mitre_subtechnique,
                        "tactics": mitre_tactic,
                        "implementation": implementation,
                    }
                )
        return value
