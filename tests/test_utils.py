import pytest

from fight_counter.utils import get_clash_data, get_clash_factor

CLASH_DATA = get_clash_data()


@pytest.mark.parametrize(
    "enemies_number,players_number,expected_clash_factor",
    (
        (1, 1, 0.5),
        (2, 1, 1),
        (2, 6, 2),
        (15, 6, 5),
        (1, 3, 1),
        (2, 3, 1.5),
        (3, 3, 2),
        (6, 3, 2),
        (7, 3, 2.5),
        (10, 3, 2.5),
        (11, 3, 3),
        (14, 3, 3),
        (15, 3, 4),
    ),
)
def test_clash_factor(
    enemies_number: int,
    players_number: int,
    expected_clash_factor: float,
):
    actual_clash_factor = get_clash_factor(
        players_number=players_number,
        enemies_number=enemies_number,
        clash_data=CLASH_DATA,
    )
    assert actual_clash_factor == expected_clash_factor
