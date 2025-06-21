from flask import Flask, jsonify, request
import requests
from typing import List, Dict, Any
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Sample station data (in production, this would come from a database)
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
        "name": "Grand Central",
        "city": "Los Angeles",
        "code": "LAX"
    },
    {
        "id": "st004",
        "name": "Penn Station",
        "city": "Philadelphia",
        "code": "PHL"
    },
    {
        "id": "st005",
        "name": "South Station",
        "city": "Boston",
        "code": "BOS"
    }
]

@app.route('/hello')
def hello():
    """Simple greeting endpoint for health checks."""
    return jsonify({'message': 'Hello, world!'})

@app.route('/stations', methods=['GET'])
def get_stations():
    """
    Get list of train stations with optional location-based filtering.
    
    Query Parameters:
        city (str, optional): Filter stations by city name (case-insensitive)
        code (str, optional): Filter stations by station code (case-insensitive)
        
    Returns:
        JSON response containing list of stations with their details.
        Each station includes: id, name, city, and code.
    
    Response Format:
        200 OK: List of station objects
        400 Bad Request: Invalid query parameters
        500 Internal Server Error: Server error occurred
    
    Example Requests:
        GET /stations - Returns all stations
        GET /stations?city=New York - Returns stations in New York
        GET /stations?code=CHI - Returns stations with code CHI
        GET /stations?city=Chicago&code=CHI - Returns stations matching both filters
    
    Example Response:
        [
            {
                "id": "st001",
                "name": "Union Station",
                "city": "New York",
                "code": "NYS"
            }
        ]
    """
    try:
        # Get query parameters
        city_filter = request.args.get('city', '').strip()
        code_filter = request.args.get('code', '').strip()
        
        logger.info(f"Fetching stations with filters - city: '{city_filter}', code: '{code_filter}'")
        
        # Validate data structure and apply filters
        filtered_stations = []
        for station in STATIONS_DATA:
            if not _validate_station_data(station):
                logger.warning(f"Invalid station data found: {station}")
                continue
            
            # Apply city filter (case-insensitive)
            if city_filter and station['city'].lower() != city_filter.lower():
                continue
                
            # Apply code filter (case-insensitive)
            if code_filter and station['code'].lower() != code_filter.lower():
                continue
            
            filtered_stations.append(station)
        
        logger.info(f"Successfully retrieved {len(filtered_stations)} stations after filtering")
        return jsonify(filtered_stations), 200
        
    except Exception as e:
        logger.error(f"Error retrieving stations: {str(e)}")
        return jsonify({
            "error": "Internal server error",
            "message": "Failed to retrieve stations"
        }), 500

def _validate_station_data(station: Dict[str, Any]) -> bool:
    """
    Validate station data structure.
    
    Args:
        station: Dictionary containing station data
        
    Returns:
        bool: True if valid, False otherwise
    """
    required_fields = ['id', 'name', 'city', 'code']
    
    if not isinstance(station, dict):
        return False
    
    for field in required_fields:
        if field not in station or not isinstance(station[field], str) or not station[field].strip():
            return False
    
    return True

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        "error": "Not found",
        "message": "The requested resource was not found"
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({
        "error": "Internal server error",
        "message": "An unexpected error occurred"
    }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80) 