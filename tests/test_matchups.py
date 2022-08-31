import pytest
from cogs.matchups import Matchups

def test_no_rows():
    output = Matchups.get_matchups.return_value = 0
    assert output == 0

def test_rows():
    output = Matchups.get_matchups.return_value = 1
    assert output == 1