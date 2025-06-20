import pytest
from src.app import app
from unittest.mock import patch, Mock

def test_hello():
    with app.test_client() as client:
        response = client.get('/hello')
        assert response.status_code == 200
        assert response.get_json() == {'message': 'Hello, world!'}

def test_stations():
    with app.test_client() as client:
        response = client.get('/stations')
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) > 0
        
        # Verify the structure of the first station
        station = data[0]
        assert 'id' in station
        assert 'name' in station
        assert 'city' in station
        assert 'code' in station
        
        # Verify specific test data
        assert station['id'] == 'st001'
        assert station['name'] == 'Union Station'
        assert station['city'] == 'New York'
        assert station['code'] == 'NYS'

def test_test_endpoint():
    with app.test_client() as client:
        response = client.get('/test')
        assert response.status_code == 200
        assert response.get_data(as_text=True) == 'this is a test'


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