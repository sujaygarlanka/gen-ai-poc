from flask import Flask, jsonify
import requests

app = Flask(__name__)

# Mock data for train stations
STATIONS_DATA = [
    {
        "id": "st001",
        "name": "Union Station",
        "city": "New York",
        "code": "NYS"
    },
    {
        "id": "st002",
        "name": "Central Station",
        "city": "Chicago",
        "code": "CHI"
    },
    {
        "id": "st003",
        "name": "Grand Central Terminal",
        "city": "New York",
        "code": "GCT"
    },
    {
        "id": "st004",
        "name": "Union Station",
        "city": "Washington",
        "code": "WAS"
    },
    {
        "id": "st005",
        "name": "30th Street Station",
        "city": "Philadelphia",
        "code": "PHL"
    },
    {
        "id": "st006",
        "name": "South Station",
        "city": "Boston",
        "code": "BOS"
    }
]

@app.route('/hello')
def hello():
    return jsonify({'message': 'Hello, world!'})

@app.route('/stations')
def get_stations():
    """Get list of all train stations"""
    return jsonify(STATIONS_DATA)

@app.route('/test')
def test():
    return 'this is a test'

@app.route('/datausa/youngest-large-county')
def datausa_youngest_large_county():
    url = 'https://datausa.io/api/data?drilldowns=County&measures=Median+Age&year=2023&order=asc&sort=Median+Age&limit=1'
    resp = requests.get(url)
    return jsonify(resp.json())

@app.route('/datausa/largest-counties')
def datausa_largest_counties():
    url = 'https://datausa.io/api/data?drilldowns=County&measures=Population&year=2023&order=desc&sort=Population&limit=5'
    resp = requests.get(url)
    return jsonify(resp.json())

@app.route('/datausa/most-expensive-housing-state')
def datausa_most_expensive_housing_state():
    url = 'https://datausa.io/api/data?drilldowns=State&measures=Median+Property+Value&year=2023&Geography=15'
    resp = requests.get(url)
    return jsonify(resp.json())

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80) 