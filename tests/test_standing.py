import pytest
from cogs.standings import Standings

def test_no_rows():
    output = Standings.get_standings.return_value = 0
    assert output == 0

def test_rows():
    output = Standings.get_standings.return_value = 1
    assert output == 1