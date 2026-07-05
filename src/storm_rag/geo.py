import geopandas as gpd, pandas as pd, glob
from pathlib import Path
from storm_rag.clean import clean

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

def load_all_events() -> pd.DataFrame:
    pattern = str(PROJECT_ROOT / "data" / "raw" / "StormEvents_details*.csv.gz")
    frames = [clean(pd.read_csv(f)) for f in glob.glob(pattern)]
    return pd.concat(frames, ignore_index=True)

def county_summary() -> gpd.GeoDataFrame:
       ev = load_all_events()
       ev["fips"] = (ev["STATE_FIPS"].astype("Int64").astype(str).str.zfill(2)
                     + ev["CZ_FIPS"].astype("Int64").astype(str).str.zfill(3))
       agg = ev.groupby("fips").agg(
           n_events=("EVENT_ID", "count"),
           total_damage=("damage_property_usd", "sum"),
       ).reset_index()
       counties = counties = gpd.read_file(str(PROJECT_ROOT / "data" / "raw" / "tl_2023_us_county.zip"))
       counties["fips"] = counties["STATEFP"] + counties["COUNTYFP"]
       return counties.merge(agg, on="fips", how="left")