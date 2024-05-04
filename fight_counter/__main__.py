import argparse

from fight_counter.enums import DifficultyLevelChoose
from fight_counter.fight_counter import FightCounter

parser = argparse.ArgumentParser(
    prog="FightCounter",
    description="Program count distribution of enemies in DnD fight",
)

parser.add_argument("players", nargs="+", help="List of players level.", type=int)

parser.add_argument("-dl", "--difficulty-level", default=DifficultyLevelChoose.COMMON)


args = parser.parse_args()


counter = FightCounter(players=args.players, difficulty_level=args.difficulty_level)

res = counter.count_distribution()

for wave, wave_full in zip(FightCounter.simplify(res), res):
    print(round(wave[0],3),":", wave[1:])
    print(wave_full)
