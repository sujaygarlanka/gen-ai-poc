import pytest
from src.app import app
from unittest.mock import patch, Mock

def test_hello():
    with app.test_client() as client:
        response = client.get('/hello')
        assert response.status_code == 200
        assert response.get_json() == {'message': 'Hello, world!'}