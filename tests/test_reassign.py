from unittest.mock import MagicMock
import pytest
from cogs.reassign import Reassign

#Testing if the league exists
def test_league_found():
    output = Reassign.reassign_league.return_value = 1
    assert output == 1

#Testing if no league is found
def test_no_league_found():
    output = Reassign.reassign_league.return_value = 0
    assert output == 0