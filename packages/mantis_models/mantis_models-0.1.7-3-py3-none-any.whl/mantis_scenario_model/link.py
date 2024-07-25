# -*- coding: utf-8 -*-
#
# Copyright (c) 2016-2021 AMOSSYS. All rights reserved.
#
# This file is part of Cyber Range AMOSSYS.
#
# Cyber Range AMOSSYS can not be copied and/or distributed without the express
# permission of AMOSSYS.
#
from typing import Any
from typing import Dict
from typing import Literal
from typing import Optional
from typing import Union

from pydantic import BaseModel
from pydantic import Field
from pydantic import IPvAnyInterface
from pydantic import root_validator
from pydantic import validator
from ruamel.yaml import YAML
from ruamel.yaml import yaml_object

from .node import Node
from .node import TypeEnum

yaml = YAML()


@yaml_object(yaml)
class NetworkConfig(BaseModel):
    ip: Optional[Union[IPvAnyInterface, Literal["dynamic"]]]
    # If the ip is not provided it should be dynamic, however it can be left empty in
    # the yaml file
    mac: Optional[str] = Field(regex="^(?:[0-9A-Fa-f]{2}[:-]){5}(?:[0-9A-Fa-f]{2})$")
    dhcp: Optional[bool]
    dhcp_nameserver: Optional[str]
    dhcp_lease: Optional[int]
    dhcp_router: Optional[str]

    @classmethod
    def to_yaml(cls, representer, node):  # noqa: ANN001, ANN206
        return representer.represent_scalar("!NetworkConfig", "u{.ip}".format(node))


@yaml_object(yaml)
class Link(BaseModel):
    switch: Node
    node: Node
    params: NetworkConfig

    @validator("switch")
    def check_is_switch(cls, v: Node) -> Node:  # noqa: ANN101, N805 TODO
        if v.type != TypeEnum.SWITCH:
            raise ValueError(f"must be of {TypeEnum.SWITCH} type")
        return v

    @validator("node")
    def check_is_not_switch(cls, v: Node) -> Node:  # noqa: ANN101, N805 TODO
        if v.type == TypeEnum.SWITCH:
            raise ValueError(f"must not be of {TypeEnum.SWITCH} type")
        return v

    @root_validator(skip_on_failure=True)
    def check_nodes_consistency(
        cls, values: Dict[str, Any]  # noqa ANN101, N805 TODO
    ) -> Dict[str, Any]:  # noqa ANN101, N805 TODO
        switch, node = values["switch"], values["node"]  # noqa ANN101, N805 TODO
        if (
            switch.type == TypeEnum.VIRTUAL_MACHINE
            and node.type == TypeEnum.VIRTUAL_MACHINE
        ):
            raise ValueError("It is not possible to link two virtual machine nodes")
        return values
