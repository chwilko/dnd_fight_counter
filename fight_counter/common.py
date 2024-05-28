import os
from typing import List, TypedDict

import choose

EXPECTED_XP_CSV = os.path.join("fight_counter", "data", "pd_levels.csv")
CLASH_DATA_JSON = os.path.join("fight_counter", "data", "clash_data.json")
CHALLENGE_XP_CSV = os.path.join("fight_counter", "data", "challenge_xp.csv")
CHALLENGE_XP_FULL_CSV = os.path.join("fight_counter", "data", "challenge_xp_full.csv")


class DifficultyLevelChoose(choose.Choices):
    EASY = choose.Choice("easy", 0)
    COMMON = choose.Choice("common", 1)
    HARD = choose.Choice("hard", 2)
    DEADLY = choose.Choice("deadly", 3)

    @classmethod
    def keys(cls):
        yield cls.EASY
        yield cls.COMMON
        yield cls.HARD
        yield cls.DEADLY


class EnemiesDict(TypedDict):
    number: int
    xp: int
    challenge: float


class WaveDict(TypedDict):
    enemies: List[EnemiesDict]
    xp: int
    expected_xp: int
    number: int
    clash_factor: float


COLORS = {
    DifficultyLevelChoose.EASY: "green",
    DifficultyLevelChoose.COMMON: "yellow",
    DifficultyLevelChoose.HARD: "orange",
    DifficultyLevelChoose.DEADLY: "red",
}
