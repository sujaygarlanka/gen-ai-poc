import pytest
from src.app import app
from unittest.mock import patch, Mock

def test_hello():
    with app.test_client() as client:
        response = client.get('/hello')
        assert response.status_code == 200
        assert response.get_json() == {'message': 'Hello, world!'}

def test_datausa_top_earning_state():
    mock_response = Mock()
    mock_response.json.return_value = {
        'data': [{'State': 'District of Columbia', 'Year': '2023', 'Median Household Income': 106287}],
        'source': []
    }
    with patch('src.app.requests.get', return_value=mock_response):
        with app.test_client() as client:
            response = client.get('/datausa/top-earning-state')
            assert response.status_code == 200
            data = response.get_json()
            assert 'data' in data
            assert data['data'][0]['State'] == 'District of Columbia'
            assert data['data'][0]['Median Household Income'] == 106287

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