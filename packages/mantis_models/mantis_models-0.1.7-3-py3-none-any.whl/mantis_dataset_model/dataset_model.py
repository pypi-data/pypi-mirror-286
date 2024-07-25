# -*- coding: utf-8 -*-
import re
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

from mantis_scenario_model.scenario_model import Scenario
from mantis_scenario_model.unit_attack_model import UnitAttack
from pydantic import BaseModel
from pydantic import validator


class ResourceType(str, Enum):
    """
    Enum for the resource type
    """

    log = "log"
    pcap = "pcap"
    memory_dump = "memory_dump"
    redteam_report = "redteam_report"
    life_report = "life_report"
    assets_report = "assets_report"
    forensic = "forensic"


class ResourceFile(BaseModel):
    """
    Model representing a file within a resource
    """

    size: int
    file_url: Path

    class Config:
        # Ensures Model Validation is performed when a member is set after the creation of the object
        validate_assignment = True


class ResourceBase(BaseModel):
    """
    Base model for all resource types
    """

    type: ResourceType
    files: List[ResourceFile]

    class Config:
        # Ensures Model Validation is performed when a member is set after the creation of the object
        validate_assignment = True


class ResourceLog(ResourceBase):
    machine: str
    log_format: str


class ResourceForensic(ResourceBase):
    machine: str
    forensic_tool: str


class ResourcePcap(ResourceBase):
    date_start: datetime
    date_end: datetime
    relationship_probe_nodes: Optional[List[dict]]


class ResourceMemoryDump(ResourceBase):
    date: datetime
    node_id: int
    dump_failure: bool


class ResourceLifeReport(ResourceBase):
    date: datetime


class ResourceAssetsReport(ResourceBase):
    date: datetime


def _pydantic_validator_mitre_tags_str(s: Any) -> "MitreTag":
    if isinstance(s, str):
        try:
            mitre_tag = MitreTag.from_mitre_str(s)
        except ValueError as e:
            assert False, str(e)
    else:
        mitre_tag = s
    return mitre_tag


def _pydantic_json_dumps_mitre_tag(
    d: Dict[str, Any], *args: List[Any], **kwargs: Dict[Any, Any]
) -> str:
    return MitreTag._dict_to_str(d)


def _pydantic_json_loads_mitre_tag(
    s: str, *args: List[Any], **kwargs: Dict[Any, Any]
) -> "MitreTag":
    return MitreTag._str_to_obj(s)


class MitreTagType(str, Enum):
    """
    Enum for the dataset mitre tags
    """

    tactic = "TA"
    technique = "T"


class MitreTag(BaseModel):
    """
    Models a MITRE ATT&CK tag for the dataset.

    Can model Tactics (e.g. TA3), Techniques (e.g. T98) or Sub-techniques (T98.002)

    This class, when serialized, is meant to be transformed into a string. For instance,
    an instance of this class with type = MitreTagType.tactic, and number = 5,
    will be represented by the string "TA5".

    Conversely, in datasets objects (or other derived models), it is allowed to specify
    MITRE tags as strings. The conversion to a MitreTag instance will be
    transparent at the loading of the JSON or dict with the `MitreTag.parse_raw`
    or `MitreTag.parse_obj` functions.
    """

    type: MitreTagType
    number: int
    subnumber: Optional[int] = None

    @classmethod
    def from_mitre_str(cls, mitre_tag_as_str: str) -> "MitreTag":
        """
        Helper function to construct a `MitreTag` object from a string (e.g. "T506.3")
        """
        return MitreTag._str_to_obj(mitre_tag_as_str)

    @classmethod
    def to_mitre_str(cls, dataset_mitre_tag: "MitreTag") -> str:
        """
        Helper function transform a `MitreTag` into its string representation (e.g. "TA05")
        """
        return MitreTag._obj_to_str(dataset_mitre_tag)

    @classmethod
    def _obj_to_str(cls, obj: "MitreTag") -> str:
        # Converts an object to its string representation
        return MitreTag._dict_to_str(obj.dict())

    @classmethod
    def _dict_to_str(cls, d: Dict[str, Any]) -> str:
        # Converts an object, transformed into dict, to its string representation
        s = d["type"].value + str(d["number"]).zfill(4)
        if d["subnumber"]:
            s += "." + str(d["subnumber"]).zfill(3)
        return s

    @classmethod
    def _str_to_obj(cls, s: str) -> "MitreTag":
        m = re.match(r"^(TA?)([0-9]{4})(\.([0-9]{3}))?$", s)
        mitre_type: Optional[MitreTagType] = None
        number: Optional[int] = None
        subnumber: Optional[int] = None
        if m:
            try:
                mitre_type = MitreTagType(m.group(1))
                number = int(m.group(2))
                if m.group(4) is not None:
                    if mitre_type is MitreTagType.tactic:
                        raise Exception()
                    else:
                        subnumber = int(m.group(4))
                return cls.parse_obj(
                    {"type": mitre_type, "number": number, "subnumber": subnumber}
                )
            except Exception:
                pass
        raise ValueError(
            f"String {s} is not recognized as a valid MITRE ATT&CK tag for Tactics (TA) or Techniques (T). Expected: TA[0-9]{4} or T[0-9]{4}(\\.[0-9]{3})?"
        )

    def __str__(self) -> str:
        return MitreTag.to_mitre_str(self)

    class Config:
        json_dumps = _pydantic_json_dumps_mitre_tag
        json_loads = _pydantic_json_loads_mitre_tag


class MitreIdName(BaseModel):
    id: Optional[MitreTag]
    name: Optional[str]
    _normalize_id = validator("id", allow_reuse=True, pre=True)(
        _pydantic_validator_mitre_tags_str
    )


class WorkerMitreData(BaseModel):
    technique: MitreIdName
    subtechnique: MitreIdName
    tactics: List[MitreIdName]


class Manifest(BaseModel):
    """
    Model for a manifest.

    Corresponds to the contents of the manifest.json file
    from version 0.4:
        - removed dataset_analysis field
    """

    manifest_version: str = "0.5"
    simu_id: int
    topology: str
    name: str
    description: Optional[str] = None
    tags: List[str] = []
    mitre_tags: Optional[List[WorkerMitreData]] = []
    date_dataset_created: datetime
    date_dataset_modified: Optional[datetime] = None
    logs: Dict[str, ResourceLog] = {}
    pcaps: Dict[str, ResourcePcap] = {}
    memory_dumps: Dict[str, ResourceMemoryDump] = {}
    redteam_reports: Dict[str, ResourceBase] = {}
    life_reports: Dict[str, ResourceLifeReport] = {}
    assets_reports: Dict[str, ResourceAssetsReport] = {}
    scenario: Optional[Union[Scenario, UnitAttack]] = None
    forensics: Optional[Dict[str, ResourceForensic]] = {}
    unit_attacks_played: List[str] = []
    scenario_config_name: Optional[str] = ""

    class Config:
        # Ensures Model Validation is performed when a member is set after the creation of the object
        validate_assignment = True


class PartialManifest(BaseModel):
    name: str
    date_dataset_created: datetime
    date_dataset_modified: Optional[datetime] = None
    tags: List[str] = []
    mitre_tags: Optional[List[WorkerMitreData]] = []
    description: Optional[str] = None
