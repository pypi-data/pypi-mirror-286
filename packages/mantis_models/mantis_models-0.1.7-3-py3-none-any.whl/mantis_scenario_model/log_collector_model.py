# -*- coding: utf-8 -*-
from enum import Enum
from typing import List

from pydantic import BaseModel


class LogCollectorStatus(str, Enum):
    development = "development"
    production = "production"


class LogCollectorLocation(str, Enum):
    node_name = "node_name"  # Allows to deploy a collector on specific node names (e.g. "Client1")
    new_node = "new_node"  # Allows to deploy a collector on a new node (e.g. a dedicated 'logstash' node)
    system_type = "system_type"  # Allows to deploy a collector on a specific system (e.g. "windows")
    operating_system = "operating_system"  # Allows to deploy a collector on a specific Windows version (e.g. "Windows 10")
    external = "external"  # Describes an external SIEM, XDR or log collector


class LogCollectorType(str, Enum):
    agent = "agent"
    aggregator = "aggregator"
    probe = "probe"
    visualization = "visualization"
    external = "external"
    # custom = "custom"  # Not yet supported


class LogCollectorUserConfig(BaseModel):
    name: str  # e.g. "collector_ip_address"
    description: str  # e.g. "IP address of the log collector."
    type: str  # Python primary type: either "str", "int", or "bool"
    default: str  # Default value
    required: bool  # Tells if the config variable is mandatory


class LogCollector(BaseModel):
    collector_name: str  # e.g. winlogbeat
    displayed_name: str  # e.g. "Winlogbeat"
    collector_type: LogCollectorType
    description: str

    status: LogCollectorStatus

    available_locations: List[LogCollectorLocation]
    available_output_collectors: List[str]  # A list of collector_name is expected here

    mandatory_inputs: List[str]  # A list of collector_name is expected here
    # This is the list of inputs needed in order for this log collector to work

    cpe_os_constraints: List[
        str
    ]  # Allows to check basebox compatibility regarding the OS, with CPE 2.3

    user_config: List[LogCollectorUserConfig]
    user_config_expert_mode: List[LogCollectorUserConfig]
