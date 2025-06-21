#!/usr/bin/env python3
"""
Integration test script for the stations endpoint.
This script demonstrates how to interact with the migrated stations endpoint.
"""

import requests
import json
import sys
from typing import List, Dict, Any

def test_stations_endpoint(base_url: str = "http://localhost:80") -> bool:
    """
    Test the stations endpoint functionality.
    
    Args:
        base_url: Base URL of the API
        
    Returns:
        bool: True if all tests pass, False otherwise
    """
    print("🚂 Testing Stations Endpoint Migration")
    print("=" * 50)
    
    try:
        # Test 1: Basic endpoint functionality
        print("Test 1: Basic GET /stations request...")
        response = requests.get(f"{base_url}/stations")
        
        if response.status_code != 200:
            print(f"❌ Failed: Expected status 200, got {response.status_code}")
            return False
        
        print("✅ Status code: 200 OK")
        
        # Test 2: Response format validation
        print("\nTest 2: Response format validation...")
        try:
            stations = response.json()
        except json.JSONDecodeError:
            print("❌ Failed: Response is not valid JSON")
            return False
        
        if not isinstance(stations, list):
            print("❌ Failed: Response should be a list")
            return False
        
        print("✅ Response is valid JSON array")
        
        # Test 3: Station data structure validation
        print("\nTest 3: Station data structure validation...")
        required_fields = ['id', 'name', 'city', 'code']
        
        for i, station in enumerate(stations):
            if not isinstance(station, dict):
                print(f"❌ Failed: Station {i} is not a dictionary")
                return False
            
            for field in required_fields:
                if field not in station:
                    print(f"❌ Failed: Station {i} missing field '{field}'")
                    return False
                
                if not isinstance(station[field], str) or not station[field].strip():
                    print(f"❌ Failed: Station {i} field '{field}' is not a valid string")
                    return False
        
        print(f"✅ All {len(stations)} stations have valid structure")
        
        # Test 4: RAML specification compliance
        print("\nTest 4: RAML specification compliance...")
        
        # Check for example stations from RAML
        station_codes = [station['code'] for station in stations]
        
        if 'NYS' not in station_codes:
            print("❌ Failed: Missing NYS station from RAML example")
            return False
        
        if 'CHI' not in station_codes:
            print("❌ Failed: Missing CHI station from RAML example")
            return False
        
        # Verify specific station details
        nys_station = next((s for s in stations if s['code'] == 'NYS'), None)
        if not nys_station:
            print("❌ Failed: NYS station not found")
            return False
        
        if nys_station['name'] != 'Union Station' or nys_station['city'] != 'New York':
            print("❌ Failed: NYS station details don't match RAML specification")
            return False
        
        print("✅ RAML specification compliance verified")
        
        # Test 5: Content type validation
        print("\nTest 5: Content type validation...")
        content_type = response.headers.get('content-type', '')
        if 'application/json' not in content_type:
            print(f"❌ Failed: Expected JSON content type, got '{content_type}'")
            return False
        
        print("✅ Correct content type: application/json")
        
        # Test 6: Method validation
        print("\nTest 6: HTTP method validation...")
        post_response = requests.post(f"{base_url}/stations")
        if post_response.status_code != 405:
            print(f"❌ Failed: POST should return 405, got {post_response.status_code}")
            return False
        
        print("✅ POST method correctly rejected with 405")
        
        # Display results
        print("\n" + "=" * 50)
        print("📊 MIGRATION RESULTS")
        print("=" * 50)
        print(f"Total stations retrieved: {len(stations)}")
        print("\nStation List:")
        for station in stations:
            print(f"  • {station['name']} ({station['code']}) - {station['city']}")
        
        print("\n✅ ALL TESTS PASSED!")
        print("🎉 Mulesoft endpoint successfully migrated to Python Flask!")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Failed: Could not connect to the API")
        print("Make sure the Flask application is running on http://localhost:80")
        return False
    except Exception as e:
        print(f"❌ Failed: Unexpected error: {str(e)}")
        return False

def demonstrate_usage_examples():
    """Demonstrate various ways to use the stations endpoint."""
    print("\n" + "=" * 50)
    print("💡 USAGE EXAMPLES")
    print("=" * 50)
    
    base_url = "http://localhost:80"
    
    try:
        # Example 1: Basic usage
        print("Example 1: Basic station retrieval")
        response = requests.get(f"{base_url}/stations")
        stations = response.json()
        print(f"Retrieved {len(stations)} stations")
        
        # Example 2: Find station by code
        print("\nExample 2: Find station by code")
        def find_station_by_code(code: str) -> Dict[str, Any]:
            for station in stations:
                if station['code'].upper() == code.upper():
                    return station
            return None
        
        nys_station = find_station_by_code('NYS')
        if nys_station:
            print(f"Found NYS: {nys_station['name']} in {nys_station['city']}")
        
        # Example 3: Group stations by city
        print("\nExample 3: Group stations by city")
        cities = {}
        for station in stations:
            city = station['city']
            if city not in cities:
                cities[city] = []
            cities[city].append(station['name'])
        
        for city, station_names in cities.items():
            print(f"  {city}: {', '.join(station_names)}")
        
        # Example 4: Create station lookup dictionary
        print("\nExample 4: Station lookup dictionary")
        station_lookup = {station['code']: station for station in stations}
        print("Available station codes:", ', '.join(station_lookup.keys()))
        
    except Exception as e:
        print(f"Error in usage examples: {str(e)}")

if __name__ == "__main__":
    print("🚂 Mulesoft to Python Flask Migration Test")
    print("Testing GET /stations endpoint migration")
    print()
    
    # Run the main test
    success = test_stations_endpoint()
    
    if success:
        # Show usage examples
        demonstrate_usage_examples()
        sys.exit(0)
    else:
        print("\n❌ Migration test failed!")
        sys.exit(1)
