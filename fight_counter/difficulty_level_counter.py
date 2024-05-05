from dataclasses import dataclass
from typing import Dict, List

from fight_counter.common import DifficultyLevelChoose
from fight_counter.utils import (
    get_challenge_xp,
    get_clash_data,
    get_clash_factor,
    get_expected_xp,
)


@dataclass
class DifficultyState:
    real_enemies_xp: int
    enemies_xp: int
    difficulty_thresholds: Dict[DifficultyLevelChoose, int]

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DifficultyState):
            return NotImplemented
        if self.real_enemies_xp != other.real_enemies_xp:
            return False
        if self.enemies_xp != other.enemies_xp:
            return False
        if self.difficulty_thresholds != other.difficulty_thresholds:
            return False
        return True


def get_enemies_exp(enemies: List[float]) -> int:
    challenge_xp = get_challenge_xp(full=True)
    enemies_xp = 0
    for enemy_challenge in enemies:
        enemies_xp += challenge_xp.loc[
            challenge_xp["challenge"] == enemy_challenge, "xp"
        ].values[0]

    return enemies_xp


def get_thresholds(players: List[int]) -> Dict[DifficultyLevelChoose, int]:
    thresholds = [0, 0, 0, 0]
    expected_xp = get_expected_xp()
    for player in players:
        for i, difficulty in enumerate(DifficultyLevelChoose.keys()):
            thresholds[i] += expected_xp.loc[
                expected_xp["player level"] == player, difficulty
            ].values[0]
    return {
        DifficultyLevelChoose.EASY: thresholds[0],
        DifficultyLevelChoose.COMMON: thresholds[1],
        DifficultyLevelChoose.HARD: thresholds[2],
        DifficultyLevelChoose.DEADLY: thresholds[3],
    }


def difficulty_counter(
    players: List[int],
    enemies: List[float],
) -> DifficultyState:
    clash_data = get_clash_data()
    enemies_xp = get_enemies_exp(enemies)
    real_enemies_xp = enemies_xp
    clash_factor = get_clash_factor(
        n_players=len(players),
        enemies_number=len(enemies),
        clash_data=clash_data,
    )
    enemies_xp = int(float(enemies_xp) // clash_factor)
    return DifficultyState(
        real_enemies_xp=real_enemies_xp,
        enemies_xp=enemies_xp,
        difficulty_thresholds=get_thresholds(players),
    )
