from typing import List

import pytest

from fight_counter.enums import DifficultyLevelChoose
from fight_counter.fight_counter import FightCounter


@pytest.mark.parametrize(
    "players, difficulty_level, expected_exp",
    (
        ([10], DifficultyLevelChoose.COMMON, 1200),
        ([1, 1, 1], DifficultyLevelChoose.COMMON, 150),
        ([1, 3, 2], DifficultyLevelChoose.EASY, 150),
        ([1, 11], DifficultyLevelChoose.HARD, 2475),
        ([4, 2, 5], DifficultyLevelChoose.DEADLY, 1800),
    ),
)
def test_sum_player_exp(
    players: List[int],
    difficulty_level: DifficultyLevelChoose,
    expected_exp: int,
):
    counter = FightCounter(players=players, difficulty_level=difficulty_level)
    assert counter.get_base_exp() == expected_exp


@pytest.mark.parametrize(
    "players, enemies_number, expected_factor",
    (
        ([1], 6, 1.5),
        ([1, 1, 1], 6, 2.0),
        ([1, 1, 1, 1, 1, 1], 6, 2.5),
        ([1, 1, 1], 20, 4.0),
        ([1, 1, 1, 1, 1, 1], 20, 5.0),
        ([1, 1], 1, 0.5),
    ),
)
def test_clash_factor(players: List[int], enemies_number: int, expected_factor: float):
    counter = FightCounter(
        players=players, difficulty_level=DifficultyLevelChoose.COMMON
    )
    assert counter._get_clash_factor(enemies_number) == expected_factor


@pytest.mark.parametrize(
    "players",
    (([1, 1, 1]),),
)
def test_run(players: List[int]):
    counter = FightCounter(
        players=players, difficulty_level=DifficultyLevelChoose.COMMON
    )
    # assert counter._get_clash_factor(enemies_number) == expected_factor
    counter.count_distribution([3])
