import pytest
from cogs.reassign import Reassign

@pytest.mark.asyncio
async def test_new_league(mocker):
   row = 1
   if row == 1:
      return mocker.patch("cogs.reassign.Reassign.reassign_league", return_value='League successfully reassigned.')   
   assert Reassign.reassign_league() == 'League successfully reassigned.' 


@pytest.mark.asyncio
async def test_no_league(mocker):
   row = 0
   if row == 0:
      return mocker.patch("cogs.reassign.Reassign.reassign_league", return_value='League name or number does not  exist, please try again with a different combination.')   
   assert Reassign.reassign_league() == 'League name or number does not  exist, please try again with a different combination.' 
