import choose


class DifficultyLevelChoose(choose.Choices):
    EASY = choose.Choice("easy", 0)
    COMMON = choose.Choice("common", 1)
    HARD = choose.Choice("hard", 2)
    DEADLY = choose.Choice("deadly", 3)
