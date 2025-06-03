import pytest
from app.etl.spacex import SpaceXAPI

@pytest.mark.asyncio
async def test_fetch_launches():
    """ Test spacex client's ability to fetch launches
    - check if api connection works
    - response contains a list of launches
    - required fields are present
    """
    api = SpaceXAPI()
    try:
        launches = await api.fetch_launches()
        assert isinstance(launches, list)
        if launches:
            assert "id" in launches[0]
            assert "name" in launches[0]
    finally:
        api.client.close() # close client even if test fails
