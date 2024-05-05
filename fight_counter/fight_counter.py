from typing import Dict, List, Optional

import numpy as np
import pandas as pd
from scipy.optimize import linprog

from fight_counter.common import DifficultyLevelChoose, EnemiesDict, WaveDict
from fight_counter.utils import (
    get_challenge_xp,
    get_clash_data,
    get_clash_factor,
    get_expected_xp,
)


class FightCounter:
    def __init__(
        self,
        players: List[int],
        difficulty_level: DifficultyLevelChoose,
    ) -> None:
        self._players = players or [1]
        self._difficulty_level = difficulty_level
        self.clash_data = self._get_clash_data()
        self._base_xp = self._count_base_xp()
        self._challenge_xp = None

    @staticmethod
    def simplify(
        counted_waves: List[WaveDict],
    ) -> List[List[float]]:
        enemies = []
        for wave in counted_waves:
            simplified = [round(wave["xp"] / float(wave["expected_xp"]), 3)]
            for enemy in wave["enemies"]:
                for _ in range(enemy["number"]):
                    simplified.append(enemy["challenge"])
            enemies.append(simplified)
        return enemies

    def get_base_xp(self) -> int:
        return self._base_xp

    @property
    def challenge_xp(self) -> pd.DataFrame:
        if self._challenge_xp is None:
            self._challenge_xp = get_challenge_xp()
        return self._challenge_xp

    def count_distribution(
        self,
        enemies_numbers: Optional[List[int]] = None,
    ) -> List[WaveDict]:
        enemies_numbers = enemies_numbers or list(range(1, 11))
        enemies: List[WaveDict] = []

        for number in enemies_numbers:
            clash_factor = self._get_clash_factor(number)
            enemies.append(self._get_wave_data(number, clash_factor))

        return enemies

    def _get_clash_data(self) -> Dict[float, List[int]]:
        return get_clash_data()

    def _get_clash_factor(self, enemies_number: int) -> float:
        return get_clash_factor(
            players_number=len(self._players),
            enemies_number=enemies_number,
            clash_data=self.clash_data,
        )

    def _count_base_xp(self) -> int:
        exp_table = get_expected_xp()
        xp = 0
        for player_level in self._players:
            xp += exp_table.loc[
                exp_table["player level"] == player_level, self._difficulty_level
            ].iloc[0]
        return xp

    def _get_wave_data(self, number: int, clash_factor: float) -> WaveDict:
        xp = int(float(self._base_xp) // clash_factor)

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
            xp=res.x.round().astype(int) @ self.challenge_xp["xp"].to_numpy(),
            expected_xp=xp,
            clash_factor=clash_factor,
        )
