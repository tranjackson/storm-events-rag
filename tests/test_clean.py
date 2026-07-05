import pandas as pd
from storm_rag.clean import parse_damage

def test_thousands(): assert parse_damage("10.00K") == 10_000
def test_millions(): assert parse_damage("1.50M") == 1_500_000
def test_billions(): assert parse_damage("2.3B") == 2_300_000_000
def test_empty(): assert parse_damage("") == 0.0
def test_nan(): assert parse_damage(pd.NA) == 0.0