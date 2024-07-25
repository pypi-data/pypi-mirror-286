# -*- coding: utf-8 -*-
from enum import Enum
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple

from pydantic import BaseModel
from pydantic import NonNegativeInt

from .log_collector_model import LogCollectorLocation
from .log_collector_model import LogCollectorType


class LogCollectorInstanceLocation(BaseModel):
    location_type: LogCollectorLocation  # e.g. LogCollectorLocation.node_name
    value: str  # e.g. "Client1"


class LogCollectorInstanceOutput(BaseModel):
    instance_name: str  # e.g. logstash01
    collector_name: str  # e.g. logstash
    collector_type: LogCollectorType  # e.g. LogCollectorType.aggregator


class LogCollectorInstance(BaseModel):
    instance_name: str  # e.g. winlogbeat_windows10
    collector_name: str  # e.g. winlogbeat
    collector_type: LogCollectorType
    location: List[LogCollectorInstanceLocation]
    # input: List[LogCollectorInput] = []  # Currently not activated
    output: List[LogCollectorInstanceOutput] = []
    user_config: Dict = (
        {}
    )  # Where keys correspond to user config names (e.g. {"collector_ip_address": "172.16.0.1"})
    user_config_expert_mode: Dict = {}


class ScenarioExecutionMode(str, Enum):
    automatic = "automatic"
    step_by_step = "step_by_step"
    custom = "custom"  # Need step_waiting_list


class PositionStep(str, Enum):
    before = "before"
    after = "after"


class ScenarioRunConfig(BaseModel):
    config_name: str = "default"
    internet_connectivity: Optional[bool] = False
    net_capture: Optional[
        bool
    ] = False  # Tells if PCAP will be generated in datasets and traffic mirrored to potential probes
    forensic_artifacts: Optional[
        bool
    ] = False  # Tells if forensic artifacts will be generated in datasets
    create_dataset: Optional[bool] = False  # Tells if a dataset will be created
    user_activity_background: Optional[
        bool
    ] = False  # Tells to produce background random user activities on desktops
    log_collectors: List[LogCollectorInstance] = []
    random_waiting_minutes: Tuple[NonNegativeInt, NonNegativeInt] = [
        0,
        0,
    ]  # Waiting range in minutes
    scenario_execution_mode: ScenarioExecutionMode = ScenarioExecutionMode.automatic
    step_waiting_list: List[str] = []
