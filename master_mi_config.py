from __future__ import annotations

from copy import deepcopy
from datetime import datetime
import json
from pathlib import Path
from typing import Any


CONFIG_FILE = Path(__file__).with_name("master_mi_config.json")


DEFAULT_CONFIG: dict[str, dict[str, Any]] = {
    "import": {
        "T90BBRM_File": "./T90-Import-20251031.xlsx",
        "IMIS_File": "Customer_IMIS_GROUP_20251031.xlsx",
        "RMAnaInfo_File": "./cdd_review_dt_wkly_20251031_Soaring.csv",
        "CSEM_USBL_File": "./cdd_cds_wkly_20251031_Soaring.csv",
        "S1_Report_Raw_File": "Stage 1 CDD Deployment-20251103.xlsx",
        "CurtArr_File": "./Master List of Payment Curtailment - 20251103.xlsx",
        "RMInfo_File": "./BAU Cust Info RM (CI to CIN) 20251103.xlsx",
        "AccClose_File": "./AccountMonitorTemplate - Ac Closed list.xlsx",
        "OffCRTAPP_File": "Off CRT Approval.xlsx",
        "QCAdj_File": "QC Adjustment - 20201231.xlsx",
        "MSC_File": "MSC_Summary_20210412.xlsx",
        "MGCSM_File": "MGCSM - 202510.xlsx",
        "MstGrp_File": "./horis_mg_202509.xlsx",
        "RAM_FileName": "Medium List 202509.xlsx",
        "HR01_File": "./HR List 202509.xlsx",
        "SCC_File": "./SCC List 202509.xlsx",
        "KPI_File": "./QVKCI7 20251102.xlsx",
        "SMS_File": "./SMS ETB 20251102.xlsx",
        "KYCOpsCM_StartDate": "2020-10-01",
        "KYCOpsCM_EndDate": "2030-12-31",
        "MICutOffDate": "2025-11-02",
    },
    "update": {
        "ReRun_Update": False,
        "MI_FileName": "GS CDD FullList Master template Full - 2025-10-31.xlsx",
        "MICutOffDate": "2025-10-30",
        "LttrArrangeT6090BeginDate": "2025-11-10",
        "LttrArrangeT6090EndDate": "2025-11-16",
        "LttrArrangeCurtEffBeginDate": "2025-11-17",
        "LttrArrangeCurtEffEndDate": "2025-11-23",
        "FCRCutoffDateMst": "2025-10-31",
        "DummyDate": "1999-01-01",
        "NoWorkers": 4,
        "ConsequeceManagementWorkflowDate": "2025-07-01",
    },
}


def _deep_update(base: dict[str, Any], overrides: dict[str, Any]) -> dict[str, Any]:
    for key, value in overrides.items():
        if isinstance(value, dict) and isinstance(base.get(key), dict):
            _deep_update(base[key], value)
        else:
            base[key] = value
    return base


def load_config(path: str | Path | None = None) -> dict[str, dict[str, Any]]:
    config = deepcopy(DEFAULT_CONFIG)
    config_path = Path(path) if path is not None else CONFIG_FILE
    if config_path.exists():
        with config_path.open("r", encoding="utf-8") as handle:
            _deep_update(config, json.load(handle))
    return config


def get_section(section: str, path: str | Path | None = None) -> dict[str, Any]:
    return load_config(path)[section]


def as_datetime(value: str | datetime) -> datetime:
    if isinstance(value, datetime):
        return value
    return datetime.fromisoformat(value)
