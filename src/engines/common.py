"""Shared definition of the benchmark job so all three engines compute exactly the same thing.

JOB: read the CSV, group by (date, platform, campaign) and sum impressions, clicks, spend, conversions, revenue
plus the row count. From this cube every platform / campaign / daily KPI can be rolled up."""
from __future__ import annotations
import pandas as pd

KEY = ["date", "platform", "campaign"]
VALUES = ["impressions", "clicks", "spend", "conversions", "revenue"]
USECOLS = KEY + VALUES
OUT_COLUMNS = KEY + ["rows"] + VALUES


def checksum(cube: pd.DataFrame) -> dict:
    """Small fingerprint used to verify that engines agree."""
    return {"groups": int(len(cube)), "rows": int(cube["rows"].sum()), "impressions": int(cube["impressions"].sum()),
            "clicks": int(cube["clicks"].sum()), "conversions": int(cube["conversions"].sum()),
            "spend": float(cube["spend"].sum()), "revenue": float(cube["revenue"].sum())}


def same(a: dict, b: dict, rel: float = 1e-9) -> bool:
    ints = all(a[k] == b[k] for k in ("groups", "rows", "impressions", "clicks", "conversions"))
    flt = all(abs(a[k] - b[k]) <= rel * max(abs(a[k]), 1.0) for k in ("spend", "revenue"))
    return ints and flt


def tidy(df: pd.DataFrame) -> pd.DataFrame:
    return df[OUT_COLUMNS].sort_values(KEY).reset_index(drop=True)
