from datetime import datetime
from app.etl.manager import ETLManager
from unittest.mock import Mock

def test_transform_launch():
    # mock db session (not used)
    mock_session = Mock()

    """ Data transformation logic test
    - Checks that the dta is transformed correctly from API format to db
    - Dates are converted to datetime objects
    - All required fields are present
    """

    # data matching API format
    sample_launch = {
        "id": "test-id",
        "name": "Test Launch",
        "flight_number": 1,
        "date_utc": "2023-01-01T00:00:00Z",
        "success": True,
        "details": "Test details",
        "rocket": "rocket-id"
    }
    
    manager = ETLManager(db=mock_session)
    result = manager.transform_launch(sample_launch)
    
    assert result["id"] == "test-id"
    assert isinstance(result["date_utc"], datetime)
    assert "created_at" in result
