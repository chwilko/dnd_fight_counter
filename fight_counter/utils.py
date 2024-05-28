import json
from typing import Dict, List

import pandas as pd

from fight_counter.common import (
    CHALLENGE_XP_CSV,
    CHALLENGE_XP_FULL_CSV,
    CLASH_DATA_JSON,
    EXPECTED_XP_CSV,
)


def get_clash_factor(
    players_number: int,
    enemies_number: int,
    clash_data: Dict[float, List[int]],
) -> float:
    factor = 4.0
    for key, list_val in clash_data.items():
        if enemies_number in list_val:
            factor = key
    if players_number >= 6:
        if factor == 1.0:
            return 0.5
        return max([i for i in clash_data.keys() if i < factor])
    if players_number < 3:
        if factor == 4.0:
            return 5.0
        return min([i for i in clash_data.keys() if i > factor])
    return factor


def get_clash_data() -> Dict[float, List[int]]:
    with open(CLASH_DATA_JSON, "r") as f:
        clash_data = dict(
            ((float(key), val) for key, val in json.loads(f.read()).items())
        )
    return clash_data


def get_expected_xp():
    return pd.read_csv(EXPECTED_XP_CSV)


def get_challenge_xp(full: bool = False):
    if full:
        return pd.read_csv(CHALLENGE_XP_FULL_CSV)
    return pd.read_csv(CHALLENGE_XP_CSV)
