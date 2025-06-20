import pytest
from src.app import app
from unittest.mock import patch, Mock

def test_hello():
    with app.test_client() as client:
        response = client.get('/hello')
        assert response.status_code == 200
        assert response.get_json() == {'message': 'Hello, world!'}

def test_test_endpoint():
    with app.test_client() as client:
        response = client.get('/test')
        assert response.status_code == 200
        assert response.get_data(as_text=True) == 'this is a test'

def test_stations_all():
    """Test getting all stations without filter"""
    with app.test_client() as client:
        response = client.get('/stations')
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) == 8  # Total number of stations in STATIONS_DATA
        
        # Check structure of first station
        station = data[0]
        assert 'id' in station
        assert 'name' in station
        assert 'city' in station
        assert 'code' in station

def test_stations_filter_by_city():
    """Test filtering stations by city"""
    with app.test_client() as client:
        # Test filtering by New York (should return 2 stations)
        response = client.get('/stations?city=New York')
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) == 2
        for station in data:
            assert station['city'] == 'New York'
        
        # Test filtering by Chicago (should return 1 station)
        response = client.get('/stations?city=Chicago')
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 1
        assert data[0]['city'] == 'Chicago'
        assert data[0]['code'] == 'CHI'

def test_stations_filter_case_insensitive():
    """Test that city filtering is case-insensitive"""
    with app.test_client() as client:
        # Test lowercase
        response = client.get('/stations?city=chicago')
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 1
        assert data[0]['city'] == 'Chicago'
        
        # Test uppercase
        response = client.get('/stations?city=BOSTON')
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 1
        assert data[0]['city'] == 'Boston'

def test_stations_filter_no_results():
    """Test filtering with city that doesn't exist"""
    with app.test_client() as client:
        response = client.get('/stations?city=NonExistentCity')
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) == 0

def test_datausa_youngest_large_county():
    mock_response = Mock()
    mock_response.json.return_value = {
        'data': [{'County': 'Utah County, UT', 'Year': '2023', 'Median Age': 25.5}],
        'source': []
    }
    with patch('src.app.requests.get', return_value=mock_response):
        with app.test_client() as client:
            response = client.get('/datausa/youngest-large-county')
            assert response.status_code == 200
            data = response.get_json()
            assert 'data' in data
            assert data['data'][0]['County'] == 'Utah County, UT'
            assert data['data'][0]['Median Age'] == 25.5

def test_datausa_largest_counties():
    mock_response = Mock()
    mock_response.json.return_value = {
        'data': [
            {'County': 'Harris County, TX', 'Year': '2023', 'Population': 4760000},
            {'County': 'Maricopa County, AZ', 'Year': '2023', 'Population': 4500000},
            {'County': 'Los Angeles County, CA', 'Year': '2023', 'Population': 9900000},
            {'County': 'Cook County, IL', 'Year': '2023', 'Population': 5200000},
            {'County': 'San Diego County, CA', 'Year': '2023', 'Population': 3300000}
        ],
        'source': []
    }
    with patch('src.app.requests.get', return_value=mock_response):
        with app.test_client() as client:
            response = client.get('/datausa/largest-counties')
            assert response.status_code == 200
            data = response.get_json()
            assert 'data' in data
            assert len(data['data']) == 5
            assert any(county['County'] == 'Harris County, TX' for county in data['data'])

def test_datausa_most_expensive_housing_state():
    mock_response = Mock()
    mock_response.json.return_value = {
        'data': [{'State': 'Hawaii', 'Year': '2023', 'Median Property Value': 808200}],
        'source': []
    }
    with patch('src.app.requests.get', return_value=mock_response):
        with app.test_client() as client:
            response = client.get('/datausa/most-expensive-housing-state')
            assert response.status_code == 200
            data = response.get_json()
            assert 'data' in data
            assert data['data'][0]['State'] == 'Hawaii'
            assert data['data'][0]['Median Property Value'] == 808200