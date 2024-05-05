from typing import List

import pytest

from fight_counter.common import DifficultyLevelChoose
from fight_counter.difficulty_level_counter import (  # DifficultyState,
    get_enemies_exp,
    get_thresholds,
)


@pytest.mark.parametrize(
    "players, easy_thresholds,common_thresholds,hard_thresholds,deadly_thresholds",
    (
        ([10], 600, 1200, 1900, 2800),
        ([10, 10], 1200, 2400, 3800, 5600),
        ([10, 1, 1], 650, 1300, 2050, 3000),
    ),
)
def test_sum_player_xp(
    players: List[int],
    easy_thresholds,
    common_thresholds,
    hard_thresholds,
    deadly_thresholds,
):
    thresholds = get_thresholds(players=players)
    assert thresholds[DifficultyLevelChoose.EASY] == easy_thresholds
    assert thresholds[DifficultyLevelChoose.COMMON] == common_thresholds
    assert thresholds[DifficultyLevelChoose.HARD] == hard_thresholds
    assert thresholds[DifficultyLevelChoose.DEADLY] == deadly_thresholds


@pytest.mark.parametrize(
    "enemies, xp",
    (
        ([1.0], 200),
        ([2.0, 0.5, 0.125], 575),
        ([10.0, 1.0, 0.0], 6110),
    ),
)
def test_sum_enemies_xp(
    enemies: List[float],
    xp: int,
):
    actual_xp = get_enemies_exp(enemies=enemies)
    assert actual_xp == xp
