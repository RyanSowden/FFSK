import pytest
from cogs.lineups import Lineups


def test_no_rows():
    output = Lineups.get_lineups = 0
    assert output == 0

def test_no_rows():
    output = Lineups.get_lineups = 1
    assert output == 1


