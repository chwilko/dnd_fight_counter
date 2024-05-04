from typing import List, TypedDict


class EnemiesDict(TypedDict):
    number: int
    xp: int
    challenge: float


class WaveDict(TypedDict):
    enemies: List[EnemiesDict]
    xp: int
    expected_xp: int
    number: int
