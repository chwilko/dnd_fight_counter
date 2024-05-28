from typing import List

import pytest

from fight_counter.common import DifficultyLevelChoose
from fight_counter.fight_counter import FightCounter


@pytest.mark.parametrize(
    "players, difficulty_level, expected_xp",
    (
        ([10], DifficultyLevelChoose.COMMON, 1200),
        ([1, 1, 1], DifficultyLevelChoose.COMMON, 150),
        ([1, 3, 2], DifficultyLevelChoose.EASY, 150),
        ([1, 11], DifficultyLevelChoose.HARD, 2475),
        ([4, 2, 5], DifficultyLevelChoose.DEADLY, 1800),
    ),
)
def test_sum_player_xp(
    players: List[int],
    difficulty_level: DifficultyLevelChoose,
    expected_xp: int,
):
    counter = FightCounter(players=players, difficulty_level=difficulty_level)
    assert counter.get_base_xp() == expected_xp


@pytest.mark.parametrize(
    "players",
    (([1, 1, 1]),),
)
def test_run(players: List[int]):
    counter = FightCounter(
        players=players, difficulty_level=DifficultyLevelChoose.COMMON
    )
    counter.count_distribution([3])
