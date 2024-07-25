# -*- coding: utf-8 -*-
from datetime import datetime
from enum import Enum
from typing import Dict
from typing import List
from typing import Optional

from pydantic import BaseModel
from pydantic import Extra

from .topology_model import Topology
from .unit_attack_model import Timestamps
from .unit_attack_model import WorkerMitreData


class ScenarioExecutionStatus(str, Enum):
    created = "CREATED"  # The task has been created but is not yet
    # totally initialized (some metadata still
    # need to be created)
    pending = "PENDING"  # The runner (Cyber Range) has not been found yet
    runner_setup = (
        "RUNNER_SETUP"  # Runner initialization (Cyber Range APIs waiting to be up)
    )
    scenario_creation = "SCENARIO_CREATION"  # Simulation is starting
    scenario_setup = (
        "SCENARIO_SETUP"  # Scenario provisioning and setup (network capture, etc.)
    )
    scenario_execution = (
        "SCENARIO_EXECUTION"  # Proper scenario exection (life and attacks)
    )
    scenario_teardown = "SCENARIO_TEARDOWN"  # After scenario execution (forensic, etc.)
    scenario_finished = "SCENARIO_FINISHED"  # Scenario has been successfully finished
    runner_teardown = "RUNNER_TEARDOWN"  # Runner is terminating
    completed = "COMPLETED"  # Scenario has been successfully finished and runner is not available anymore
    cancelled = "CANCELLED"  # Scenario has been cancelled
    error = "ERROR"  # Scenario triggered an internal error
    pause = "PAUSE"  # Scenario pause


class ScenarioExecutionStopped(Exception):
    pass


class Compromise(BaseModel):
    target_name: str = "target"
    target_os: Optional[str] = None
    communication_protocol: Optional[str] = None
    username: str
    password: str
    init_knowledge: Optional[List[str]] = None
    execute_attack: Optional[List[str]]


class TopologyScenario(BaseModel):
    file: str
    deploy: bool = False
    docker_nodes: Optional[List[str]] = []
    yaml: str = None  # type: ignore
    topology: Topology = None  # type: ignore


class Steps(BaseModel):
    skip_deploy: bool = False
    skip_all_preparations: bool = False
    skip_provisioning_os_set_time: bool = False
    skip_provisioning_os_set_hostname: bool = False
    skip_provisioning_attack: bool = False
    skip_provisioning_os_monitoring: bool = False
    skip_user_activity: bool = False
    skip_compromise: bool = False
    skip_attack: bool = False
    skip_create_dataset: bool = False


class Scenario(BaseModel):
    name: str = "default scenario name"
    keywords: List[str] = []
    description: str = ""
    description_fr: str = ""
    long_description: List[str] = []
    long_description_fr: List[str] = []
    compromise: Optional[Compromise] = None  # type: ignore
    unit_attacks: List[str] = []
    mitre_tags: Optional[List[WorkerMitreData]] = []
    topology: TopologyScenario = {}
    steps: Optional[Steps] = Steps()
    timestamps: Optional[Timestamps] = None
    scenario_config: List[Dict] = []
    creation_date: datetime
    last_update: datetime

    class Config:
        extra = Extra.forbid
        validate_assignment = True
