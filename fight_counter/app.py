import base64
import io
import os

import matplotlib.pyplot as plt
from flask import Flask, render_template, request

from fight_counter.common import DifficultyLevelChoose
from fight_counter.difficulty_level_counter import difficulty_counter

app = Flask(__name__)

TEMPLATES_PATH = ["fight_counter", "templates"]
COLORS = {
    DifficultyLevelChoose.EASY: "green",
    DifficultyLevelChoose.COMMON: "yellow",
    DifficultyLevelChoose.HARD: "orange",
    DifficultyLevelChoose.DEADLY: "red",
}


def complete_path(file_name: str) -> str:
    return os.path.join(*TEMPLATES_PATH, file_name)


def make_sq(val1, val2):
    return [
        val1,
        val1,
        val2,
        val2,
    ]


@app.route("/")
def index():
    return render_template("difficulty_level_counter.html", plot_image="")


@app.route("/generate_plot", methods=["POST"])
def generate_plot():
    try:
        players = [int(x) for x in request.form["players"].split(",")]
        enemies = [float(y) for y in request.form["enemies"].split(",")]
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
        plot_url = base64.b64encode(img.getvalue()).decode()

        return render_template("difficulty_level_counter.html", plot_image=plot_url)
    except ValueError:
        return "Enter the correct number values separated by commas."


if __name__ == "__main__":
    app.run(debug=True)
