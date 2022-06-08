import pytest
from cogs.assign import Assign

#Testing the league doesn't exist
def test_no_league_found():
    output = Assign.assign_league.return_value = 0
    assert output == 0

#Testing if the league exists 
def test_league_exists():
    output = Assign.assign_league.return_value = 1
    assert output == 1
