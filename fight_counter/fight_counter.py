import json
import os
from typing import Dict, List, Optional, TypedDict

import numpy as np
import pandas as pd
from scipy.optimize import linprog

from .enums import DifficultyLevelChoose


class EnemiesDict(TypedDict):
    number: int
    xp: int
    challenge: float


class WaveDict(TypedDict):
    enemies: List[EnemiesDict]
    xp: int
    expected_xp: int
    number: int


class FightCounter:
    EXPECTED_EXP_CSV = os.path.join("fight_counter", "data", "pd_levels.csv")
    CLASH_DATA_JSON = os.path.join("fight_counter", "data", "clash_data.json")
    CHALLENGE_XP_CSV = os.path.join("fight_counter", "data", "challenge_xp.csv")

    def __init__(
        self, players: List[int], difficulty_level: DifficultyLevelChoose
    ) -> None:
        self._players = players or [1]
        self._difficulty_level = difficulty_level
        self.clash_data = self._get_clash_data()
        self._base_exp = self._count_base_exp()
        self._challenge_xp = None

    def get_base_exp(self):
        return self._base_exp

    @property
    def challenge_xp(self) -> pd.DataFrame:
        if self._challenge_xp is None:
            self._challenge_xp = pd.read_csv(self.CHALLENGE_XP_CSV)
        return self._challenge_xp

    def _get_clash_data(self) -> Dict[float, List[int]]:
        with open(self.CLASH_DATA_JSON, "r") as f:
            clash_data = dict(
                ((float(key), val) for key, val in json.loads(f.read()).items())
            )
        return clash_data

    def _get_clash_factor(self, enemies_number: int) -> float:
        factor = 4.0
        for key, list_val in self.clash_data.items():
            if enemies_number in list_val:
                factor = key
        n_players = len(self._players)
        if n_players < 3:
            if factor == 1.0:
                return 0.5
            return max([i for i in self.clash_data.keys() if i < factor])
        if n_players >= 6:
            if factor == 4.0:
                return 5.0
            return min([i for i in self.clash_data.keys() if i > factor])
        return factor

    def _count_base_exp(self) -> int:
        exp_table = pd.read_csv(self.EXPECTED_EXP_CSV)
        xp = 0
        for player_level in self._players:
            xp += exp_table.loc[
                exp_table["player level"] == player_level, self._difficulty_level
            ].iloc[0]
        return xp

    def count_distribution(self, enemies_numbers: Optional[List[int]] = None):
        enemies_numbers = enemies_numbers or list(range(1, 11))
        enemies: List[WaveDict] = []

        for number in enemies_numbers:
            clash_factor = self._get_clash_factor(number)
            enemies.append(self._get_wave_data(number, clash_factor))

        return (enemies,)

    def _get_wave_data(self, number: int, clash_factor: float):
        xp = int(self._base_exp * clash_factor)

        minimizer_vec = self.challenge_xp["xp"].to_numpy()
        challenge_xp = np.array([minimizer_vec])
        n = len(minimizer_vec)
        res = linprog(
            minimizer_vec,
            A_ub=-challenge_xp,
            b_ub=np.array([[-xp]]),
            A_eq=np.ones([1, n]),
            b_eq=np.array([[number]]),
            integrality=1,
        )

        enemies: List[EnemiesDict] = []
        for i, count in enumerate(res.x.astype(int)):
            if count == 0:
                continue
            data = self.challenge_xp.iloc[i].to_dict()
            enemies.append(
                EnemiesDict(number=count, challenge=data["challenge"], xp=data["xp"])
            )

        return WaveDict(
            enemies=enemies,
            number=number,
            xp=res.x.astype(int) @ self.challenge_xp["xp"].to_numpy(),
            expected_xp=xp,
        )
