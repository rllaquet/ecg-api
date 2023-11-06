import pytest

from utils.ecg_tools import zero_crossings


@pytest.mark.parametrize(
    "signal, expected_zero_crossings",
    [
        ([1, 2, 3, 4, 5], 0),
        ([2, 1, 0, -1, -2], 1),
        ([1, -1, 2, -2, 3, -3, 4, -4, 5, -5, -3], 9),
        ([1, 0, 1], 0),
        ([-1, 0, -1], 0),
        ([3, 2, 0, 0, -1], 1),
        ([-3, -2, 0, 0, 1], 1),
        ([-3, 0], 0),
        ([0], 0),
        ([], 0),
    ],
)
def test_zero_crossings(signal, expected_zero_crossings):
    assert zero_crossings(signal) == expected_zero_crossings
