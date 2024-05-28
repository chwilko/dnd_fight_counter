import os

from flask import Flask, render_template, request

from .plot_maker import get_difficulty_plot, get_stats_plot

app = Flask(__name__)

TEMPLATES_PATH = ["fight_counter", "templates"]


def complete_path(file_name: str) -> str:
    return os.path.join(*TEMPLATES_PATH, file_name)


@app.route("/")
def index():
    return render_template("difficulty_level_counter.html", plot_image="")


@app.route("/generate_plot", methods=["POST"])
def generate_plot():
    try:
        players = [int(x) for x in request.form["players"].split(",")]
        enemies = [float(y) for y in request.form["enemies"].split(",")]
        plot_url = get_difficulty_plot(players, enemies)
        stats_plot_url = get_stats_plot(players, enemies)
        return render_template(
            "difficulty_level_counter.html",
            plot_image=plot_url,
            stats_plot=stats_plot_url,
        )
    except ValueError:
        return "Enter the correct number values separated by commas."


if __name__ == "__main__":
    app.run(debug=True)
