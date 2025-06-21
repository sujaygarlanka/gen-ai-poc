import pytest
from src.app import app, _validate_station_data
from unittest.mock import patch, Mock
import json

@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_hello(client):
    """Test the hello endpoint."""
    response = client.get('/hello')
    assert response.status_code == 200
    assert response.get_json() == {'message': 'Hello, world!'}

def test_get_stations_success(client):
    """Test successful retrieval of stations."""
    response = client.get('/stations')
    assert response.status_code == 200
    
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0
    
    # Verify first station structure
    station = data[0]
    assert 'id' in station
    assert 'name' in station
    assert 'city' in station
    assert 'code' in station
    
    # Verify expected data
    expected_station = {
        "id": "st001",
        "name": "Union Station",
        "city": "New York",
        "code": "NYS"
    }
    assert station == expected_station

def test_get_stations_content_type(client):
    """Test that stations endpoint returns correct content type."""
    response = client.get('/stations')
    assert response.status_code == 200
    assert response.content_type == 'application/json'

def test_get_stations_all_required_fields(client):
    """Test that all stations have required fields."""
    response = client.get('/stations')
    assert response.status_code == 200
    
    data = response.get_json()
    required_fields = ['id', 'name', 'city', 'code']
    
    for station in data:
        for field in required_fields:
            assert field in station
            assert isinstance(station[field], str)
            assert station[field].strip() != ""

def test_get_stations_method_not_allowed(client):
    """Test that POST method is not allowed on stations endpoint."""
    response = client.post('/stations')
    assert response.status_code == 405

def test_validate_station_data_valid():
    """Test station data validation with valid data."""
    valid_station = {
        "id": "st001",
        "name": "Test Station",
        "city": "Test City",
        "code": "TST"
    }
    assert _validate_station_data(valid_station) == True

def test_validate_station_data_missing_field():
    """Test station data validation with missing required field."""
    invalid_station = {
        "id": "st001",
        "name": "Test Station",
        "city": "Test City"
        # Missing 'code' field
    }
    assert _validate_station_data(invalid_station) == False

def test_validate_station_data_empty_field():
    """Test station data validation with empty field."""
    invalid_station = {
        "id": "st001",
        "name": "",  # Empty name
        "city": "Test City",
        "code": "TST"
    }
    assert _validate_station_data(invalid_station) == False

def test_validate_station_data_whitespace_field():
    """Test station data validation with whitespace-only field."""
    invalid_station = {
        "id": "st001",
        "name": "   ",  # Whitespace only
        "city": "Test City",
        "code": "TST"
    }
    assert _validate_station_data(invalid_station) == False

def test_validate_station_data_non_string_field():
    """Test station data validation with non-string field."""
    invalid_station = {
        "id": 123,  # Non-string id
        "name": "Test Station",
        "city": "Test City",
        "code": "TST"
    }
    assert _validate_station_data(invalid_station) == False

def test_validate_station_data_not_dict():
    """Test station data validation with non-dictionary input."""
    assert _validate_station_data("not a dict") == False
    assert _validate_station_data(None) == False
    assert _validate_station_data([]) == False

@patch('src.app.STATIONS_DATA')
def test_get_stations_server_error(mock_stations_data, client):
    """Test stations endpoint handles server errors gracefully."""
    # Make STATIONS_DATA raise an exception when accessed
    mock_stations_data.__iter__.side_effect = Exception("Database connection failed")
    
    response = client.get('/stations')
    assert response.status_code == 500
    
    data = response.get_json()
    assert 'error' in data
    assert 'message' in data
    assert data['error'] == 'Internal server error'

def test_404_error_handler(client):
    """Test 404 error handler."""
    response = client.get('/nonexistent-endpoint')
    assert response.status_code == 404
    
    data = response.get_json()
    assert 'error' in data
    assert 'message' in data
    assert data['error'] == 'Not found'

def test_stations_response_structure(client):
    """Test that stations response matches expected RAML structure."""
    response = client.get('/stations')
    assert response.status_code == 200
    
    data = response.get_json()
    
    # Verify it's an array of Station objects as per RAML
    assert isinstance(data, list)
    
    for station in data:
        # Each station should match the Station type from RAML
        assert isinstance(station, dict)
        assert len(station) == 4  # id, name, city, code
        
        # Verify field types
        assert isinstance(station['id'], str)
        assert isinstance(station['name'], str)
        assert isinstance(station['city'], str)
        assert isinstance(station['code'], str)

def test_stations_example_data_matches_raml(client):
    """Test that response includes the example data from RAML specification."""
    response = client.get('/stations')
    assert response.status_code == 200
    
    data = response.get_json()
    
    # Check for the example stations from RAML
    station_codes = [station['code'] for station in data]
    assert 'NYS' in station_codes
    assert 'CHI' in station_codes
    
    # Find and verify the specific example stations
    nys_station = next((s for s in data if s['code'] == 'NYS'), None)
    chi_station = next((s for s in data if s['code'] == 'CHI'), None)
    
    assert nys_station is not None
    assert nys_station['name'] == 'Union Station'
    assert nys_station['city'] == 'New York'
    
    assert chi_station is not None
    assert chi_station['name'] == 'Central Station'
    assert chi_station['city'] == 'Chicago'

def test_filter_stations_by_city(client):
    """Test filtering stations by city."""
    response = client.get('/stations?city=New York')
    assert response.status_code == 200
    
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]['city'] == 'New York'
    assert data[0]['name'] == 'Union Station'

def test_filter_stations_by_city_case_insensitive(client):
    """Test filtering stations by city is case insensitive."""
    response = client.get('/stations?city=new york')
    assert response.status_code == 200
    
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['city'] == 'New York'

def test_filter_stations_by_code(client):
    """Test filtering stations by code."""
    response = client.get('/stations?code=CHI')
    assert response.status_code == 200
    
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]['code'] == 'CHI'
    assert data[0]['name'] == 'Central Station'

def test_filter_stations_by_code_case_insensitive(client):
    """Test filtering stations by code is case insensitive."""
    response = client.get('/stations?code=chi')
    assert response.status_code == 200
    
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['code'] == 'CHI'

def test_filter_stations_by_city_and_code(client):
    """Test filtering stations by both city and code."""
    response = client.get('/stations?city=Chicago&code=CHI')
    assert response.status_code == 200
    
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['city'] == 'Chicago'
    assert data[0]['code'] == 'CHI'

def test_filter_stations_no_matches(client):
    """Test filtering stations with no matches returns empty list."""
    response = client.get('/stations?city=NonExistentCity')
    assert response.status_code == 200
    
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 0

def test_filter_stations_conflicting_filters(client):
    """Test filtering with conflicting filters returns empty list."""
    response = client.get('/stations?city=New York&code=CHI')
    assert response.status_code == 200
    
    data = response.get_json()
    assert len(data) == 0

def test_filter_stations_empty_parameters(client):
    """Test filtering with empty parameters returns all stations."""
    response = client.get('/stations?city=&code=')
    assert response.status_code == 200
    
    data = response.get_json()
    assert len(data) == 5  # All stations should be returned

def test_filter_stations_whitespace_parameters(client):
    """Test filtering with whitespace-only parameters returns all stations."""
    response = client.get('/stations?city=   &code=   ')
    assert response.status_code == 200
    
    data = response.get_json()
    assert len(data) == 5  # All stations should be returned