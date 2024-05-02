import json
import os
from typing import Callable, Dict, List, Optional

import pandas as pd

from .enums import DifficultyLevelChoose


class FightCounter:
    EXPECTED_EXP_CSV = os.path.join("data", "challenge_xp.csv")
    CLASH_DATA_JSON = os.path.join("data", "clash_data.json")

    def __init__(
        self,
        players: Optional[List[int]],
        difficulty_level: DifficultyLevelChoose = DifficultyLevelChoose.COMMON,
    ) -> None:
        self.players = players or [1]
        self.difficulty_level = difficulty_level
        self.clash_data = self.get_clash_data()


    def set_difficultly_level(
        self,
        difficultly_level: DifficultyLevelChoose,
    ) -> None:
        self.difficultly_level = difficultly_level

    def set_players(
        self,
        players: List[int],
    ) -> None:
        self.players = players

    def get_clash_data(self) -> Dict[int, List[int]]:
        with open(self.CLASH_DATA_JSON, "r") as f:
            clash_data = dict(
                ((float(key), val) for key, val in json.dumps(f.read()).items())
            )
        return clash_data

    def get_clash_factor(self, enemies_number: int) -> float:
        clash = self.clash_data
        factor = 4
        for key, list_val in clash.items():
            if enemies_number in list_val:
                factor = key
        n_players = len(self.players)
        if n_players < 3:
            if factor == 1.0:
                return 0.5
            return max([i for i in clash.keys() if i < factor])
        if n_players >= 6:
            if factor == 4.0:
                return 5.0
            return min([i for i in clash.keys() if i > factor])
        return factor

    def get_expected_fight_exp(self):
        exp_table = json.dumps(self.CLASH_DATA_JSON)

    