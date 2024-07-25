# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Dict
from typing import List

from mantis_dataset_model.dataset_model import WorkerMitreData
from pydantic import BaseModel


class Worker(BaseModel):
    id: str
    name: str
    description: str
    cve: List[Dict[str, str]]
    stability: str
    reliability: str
    side_effect: str
    killchain_step: str
    repeatable: str
    mitre_data: WorkerMitreData


class Attack(BaseModel):
    id: str
    source_id: str
    worker: Worker
    status: str
    started_date: datetime
    last_update: datetime
    target_nodes: List[str]
    output: List[str]
    infrastructure: List[str]
