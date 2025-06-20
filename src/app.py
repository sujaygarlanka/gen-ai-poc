from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Sample train stations data
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
        "city": "Los Angeles",
        "code": "LAX"
    },
    {
        "id": "st005",
        "name": "South Station",
        "city": "Boston",
        "code": "BOS"
    },
    {
        "id": "st006",
        "name": "30th Street Station",
        "city": "Philadelphia",
        "code": "PHL"
    },
    {
        "id": "st007",
        "name": "Union Station",
        "city": "Washington DC",
        "code": "WAS"
    },
    {
        "id": "st008",
        "name": "King Street Station",
        "city": "Seattle",
        "code": "SEA"
    }
]

@app.route('/stations')
def get_stations():
    """
    Get list of all train stations with optional city filtering
    Query Parameters:
    - city: Filter stations by city name (case-insensitive)
    """
    try:
        # Get city filter parameter
        city_filter = request.args.get('city')
        
        # Start with all stations
        stations = STATIONS_DATA.copy()
        
        # Apply city filter if provided
        if city_filter:
            stations = [
                station for station in stations 
                if station['city'].lower() == city_filter.lower()
            ]
        
        return jsonify(stations), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500

@app.route('/hello')
def hello():
    return jsonify({'message': 'Hello, world!'})

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