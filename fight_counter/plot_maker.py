import base64
import io
from typing import List, TypeVar

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

from fight_counter.common import COLORS, DifficultyLevelChoose
from fight_counter.difficulty_level_counter import difficulty_counter

NumberVar = TypeVar("NumberVar", int, float)


def make_sq(val1, val2):
    return [
        val1,
        val1,
        val2,
        val2,
    ]


def get_difficulty_plot(players: List[int], enemies: List[float]) -> str:
    difficulty = difficulty_counter(players=players, enemies=enemies)
    thresholds = difficulty.difficulty_thresholds
    X = [0, 1]
    X_sq = [0, 1, 1, 0]
    ylim = [
        min(
            thresholds[DifficultyLevelChoose.EASY],
            difficulty.enemies_xp * 9 // 10,
        ),
        max(
            2 * thresholds[DifficultyLevelChoose.DEADLY]
            - thresholds[DifficultyLevelChoose.HARD],
            difficulty.enemies_xp * 11 // 10,
        ),
    ]
    _ = plt.figure()
    plt.fill(
        X_sq,
        make_sq(
            thresholds[DifficultyLevelChoose.EASY],
            thresholds[DifficultyLevelChoose.COMMON],
        ),
        color=COLORS[DifficultyLevelChoose.EASY],
        label=f"Difficult: {DifficultyLevelChoose.EASY}",
    )
    plt.fill(
        X_sq,
        make_sq(
            thresholds[DifficultyLevelChoose.COMMON],
            thresholds[DifficultyLevelChoose.HARD],
        ),
        color=COLORS[DifficultyLevelChoose.COMMON],
        label=f"Difficult: {DifficultyLevelChoose.COMMON}",
    )
    plt.fill(
        X_sq,
        make_sq(
            thresholds[DifficultyLevelChoose.HARD],
            thresholds[DifficultyLevelChoose.DEADLY],
        ),
        color=COLORS[DifficultyLevelChoose.HARD],
        label=f"Difficult: {DifficultyLevelChoose.HARD}",
    )
    plt.fill(
        X_sq,
        make_sq(
            thresholds[DifficultyLevelChoose.DEADLY],
            2 * thresholds[DifficultyLevelChoose.DEADLY]
            - thresholds[DifficultyLevelChoose.COMMON],
        ),
        color=COLORS[DifficultyLevelChoose.DEADLY],
        label=f"Difficult: {DifficultyLevelChoose.DEADLY}",
    )

    plt.plot(
        [0.5], [difficulty.enemies_xp], "*", c="k", label=f"{difficulty.enemies_xp}"
    )

    plt.xlim(X)
    plt.ylim(ylim)
    plt.ylabel("scaled xp")
    plt.xticks([])
    plt.yticks(sorted(difficulty.difficulty_thresholds.values()))
    plt.legend()
    plt.title(f"Real fight xp: {difficulty.real_enemies_xp}")

    img = io.BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode()




def get_stats_plot(players: List[int], enemies: List[float]) -> str:
    _ = plt.figure()
    plt.subplot(211)
    plt.hist(enemies)
    plt.title("Enemies")
    plt.xticks(list(set(enemies)))
    plt.grid(True)
    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))

    plt.subplot(212)
    plt.hist(players)
    plt.title("Characters")
    plt.xticks(list(set(players)))
    plt.grid(True)
    plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))

    img = io.BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode()
