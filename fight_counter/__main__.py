import argparse

from fight_counter.app import app
from fight_counter.common import DifficultyLevelChoose
from fight_counter.fight_counter import FightCounter

parser = argparse.ArgumentParser(
    prog="FightCounter",
    description="Program count distribution of enemies in DnD fight",
)

parser.add_argument("players", nargs="*", help="List of players level.", type=int)

parser.add_argument("-dl", "--difficulty-level", default=DifficultyLevelChoose.COMMON)
parser.add_argument(
    "--enemies-number",
    nargs="*",
    help="List of enemy numbers.",
    default=None,
    type=int,
)
parser.add_argument("--run-gui", type=bool, default=False)


args = parser.parse_args()
if args.run_gui:
    app.run()
    exit()


counter = FightCounter(players=args.players, difficulty_level=args.difficulty_level)

res = counter.count_distribution(args.enemies_number)

for wave, wave_full in zip(FightCounter.simplify(res), res):
    print(round(wave[0], 3), ":", wave[1:])
    print(wave_full)
