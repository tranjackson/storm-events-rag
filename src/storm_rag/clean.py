import pandas as pd

_MULT = {"K": 1_000, "M": 1_000_000, "B": 1_000_000_000}

def parse_damage(val: str | float) -> float:
       """'10.00K' -> 10000.0 ; '' / NaN -> 0.0"""
       if pd.isna(val) or val == "":
           return 0.0
       s = str(val).strip().upper()
       if s[-1] in _MULT:
           return float(s[:-1]) * _MULT[s[-1]]
       return float(s)

def clean(df: pd.DataFrame) -> pd.DataFrame:
       df = df.copy()
       df["damage_property_usd"] = df["DAMAGE_PROPERTY"].map(parse_damage)
       df["damage_crops_usd"] = df["DAMAGE_CROPS"].map(parse_damage)
       df["begin_dt"] = pd.to_datetime(df["BEGIN_DATE_TIME"], format="%d-%b-%y %H:%M:%S", errors="coerce")
       df["event_type"] = df["EVENT_TYPE"].str.strip().str.title()
       return df