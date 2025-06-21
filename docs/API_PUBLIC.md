# Gen AI POC - Public API Documentation

Welcome to the Gen AI POC API documentation. This document provides comprehensive information for developers who want to integrate with our Flask API.

## 🌐 API Overview

The Gen AI POC API is a RESTful service built with Flask that provides simple, reliable endpoints for development and testing purposes, including train station management functionality.

### Base URLs
- **Development**: `http://localhost:80`
- **Staging**: `https://staging.gen-ai-poc.com` (coming soon)
- **Production**: `https://api.gen-ai-poc.com` (coming soon)

### API Version
Current version: **v1.0**

## 🔐 Authentication

Currently, no authentication is required for any endpoints. All endpoints are publicly accessible.

## 📡 Response Format

All API responses follow a consistent JSON format:

```json
{
  "message": "Response data"
}
```

## ⚠️ Error Handling

The API uses standard HTTP status codes and returns error messages in JSON format.

### Common Error Responses

**400 Bad Request**
```json
{
  "error": "Bad Request",
  "message": "Invalid request parameters"
}
```

**404 Not Found**
```json
{
  "error": "Not Found", 
  "message": "The requested endpoint was not found"
}
```

**500 Internal Server Error**
```json
{
  "error": "Internal Server Error",
  "message": "An unexpected error occurred"
}
```

## 📋 Available Endpoints

### Hello Endpoint

**GET** `/hello`

A simple greeting endpoint that returns a welcome message.

#### Request
```bash
curl -X GET https://api.gen-ai-poc.com/hello
```

#### Response
**Status Code:** `200 OK`

```json
{
  "message": "Hello, world!"
}
```

### Stations Endpoint

**GET** `/stations`

Retrieves a list of train stations with optional location-based filtering.

#### Query Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `city` | string | No | Filter stations by city name (case-insensitive) |
| `code` | string | No | Filter stations by station code (case-insensitive) |

#### Request Examples
```bash
# Get all stations
curl -X GET https://api.gen-ai-poc.com/stations

# Filter by city
curl -X GET "https://api.gen-ai-poc.com/stations?city=New York"

# Filter by code
curl -X GET "https://api.gen-ai-poc.com/stations?code=CHI"

# Filter by both city and code
curl -X GET "https://api.gen-ai-poc.com/stations?city=Chicago&code=CHI"
```

#### Response
**Status Code:** `200 OK`

```json
[
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
```

#### Station Object Structure
| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier for the station |
| `name` | string | Full name of the station |
| `city` | string | City where the station is located |
| `code` | string | Short code identifier for the station |

#### Filtering Behavior
- **Case Insensitive**: All filters are case-insensitive
- **Exact Match**: Filters require exact matches (not partial)
- **Multiple Filters**: When multiple filters are provided, stations must match ALL criteria
- **Empty Results**: Returns empty array if no stations match the criteria
- **Empty Parameters**: Empty or whitespace-only parameters are ignored

#### Error Responses
**500 Internal Server Error**
```json
{
  "error": "Internal server error",
  "message": "Failed to retrieve stations"
}
```

## 📝 Example Usage

### Hello Endpoint Examples

**JavaScript (Fetch API)**
```javascript
fetch('https://api.gen-ai-poc.com/hello')
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then(data => {
    console.log('Greeting:', data.message);
  })
  .catch(error => {
    console.error('Error:', error);
  });
```

**Python (Requests)**
```python
import requests

def get_greeting():
    try:
        response = requests.get('https://api.gen-ai-poc.com/hello')
        response.raise_for_status()
        data = response.json()
        return data['message']
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

greeting = get_greeting()
print(greeting)  # "Hello, world!"
```

### Stations Endpoint Examples

**JavaScript (Fetch API)**
```javascript
async function getStations(filters = {}) {
  try {
    // Build query string from filters
    const queryParams = new URLSearchParams();
    if (filters.city) queryParams.append('city', filters.city);
    if (filters.code) queryParams.append('code', filters.code);
    
    const url = `https://api.gen-ai-poc.com/stations${queryParams.toString() ? '?' + queryParams.toString() : ''}`;
    const response = await fetch(url);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const stations = await response.json();
    
    // Display stations
    stations.forEach(station => {
      console.log(`${station.name} (${station.code}) - ${station.city}`);
    });
    
    return stations;
  } catch (error) {
    console.error('Error fetching stations:', error);
    throw error;
  }
}

// Usage examples
getStations(); // Get all stations
getStations({ city: 'New York' }); // Get stations in New York
getStations({ code: 'CHI' }); // Get stations with code CHI
getStations({ city: 'Chicago', code: 'CHI' }); // Get stations matching both filters
```

**Python (Requests)**
```python
import requests

def get_stations(city=None, code=None):
    """Fetch train stations with optional filtering."""
    try:
        params = {}
        if city:
            params['city'] = city
        if code:
            params['code'] = code
            
        response = requests.get('https://api.gen-ai-poc.com/stations', params=params)
        response.raise_for_status()
        stations = response.json()
        
        # Display stations
        for station in stations:
            print(f"{station['name']} ({station['code']}) - {station['city']}")
        
        return stations
    except requests.exceptions.RequestException as e:
        print(f"Error fetching stations: {e}")
        return []

def find_stations_by_city(city):
    """Find all stations in a specific city."""
    return get_stations(city=city)

def find_station_by_code(code):
    """Find a station by its code."""
    stations = get_stations(code=code)
    return stations[0] if stations else None

# Usage examples
all_stations = get_stations()
print(f"Total stations: {len(all_stations)}")

# Filter by city
ny_stations = find_stations_by_city('New York')
print(f"Stations in New York: {len(ny_stations)}")

# Find specific station
chi_station = find_station_by_code('CHI')
if chi_station:
    print(f"Found: {chi_station['name']} in {chi_station['city']}")

# Case insensitive filtering
stations_lower = get_stations(city='new york')
print(f"Case insensitive search found: {len(stations_lower)} stations")
```

**Python (aiohttp - Async)**
```python
import aiohttp
import asyncio

async def get_stations_async(city=None, code=None):
    """Asynchronously fetch train stations with optional filtering."""
    async with aiohttp.ClientSession() as session:
        try:
            params = {}
            if city:
                params['city'] = city
            if code:
                params['code'] = code
                
            async with session.get('https://api.gen-ai-poc.com/stations', params=params) as response:
                if response.status == 200:
                    stations = await response.json()
                    return stations
                else:
                    raise Exception(f"HTTP {response.status}")
        except Exception as e:
            print(f"Error: {e}")
            return []

# Usage
async def main():
    all_stations = await get_stations_async()
    print(f"Retrieved {len(all_stations)} stations")
    
    ny_stations = await get_stations_async(city='New York')
    print(f"New York stations: {len(ny_stations)}")

asyncio.run(main())
```

**cURL Examples**
```bash
# Get all stations
curl https://api.gen-ai-poc.com/stations

# Filter by city
curl "https://api.gen-ai-poc.com/stations?city=New%20York"

# Filter by code
curl "https://api.gen-ai-poc.com/stations?code=CHI"

# Filter by both (URL encoded)
curl "https://api.gen-ai-poc.com/stations?city=Chicago&code=CHI"

# Case insensitive filtering
curl "https://api.gen-ai-poc.com/stations?city=new%20york"

# Pretty print filtered results
curl "https://api.gen-ai-poc.com/stations?city=Chicago" | python -m json.tool

# Save filtered results to file
curl "https://api.gen-ai-poc.com/stations?code=NYS" -o ny_station.json
```

**Node.js (Express Integration)**
```javascript
const express = require('express');
const axios = require('axios');
const app = express();

// Endpoint to get stations with filtering
app.get('/api/stations', async (req, res) => {
  try {
    const { city, code } = req.query;
    const params = {};
    
    if (city) params.city = city;
    if (code) params.code = code;
    
    const response = await axios.get('https://api.gen-ai-poc.com/stations', { params });
    const stations = response.data;
    
    res.json({
      total: stations.length,
      filters: params,
      stations: stations
    });
  } catch (error) {
    console.error('Error fetching stations:', error);
    res.status(500).json({ error: 'Failed to fetch stations' });
  }
});

// Endpoint to get stations by city
app.get('/api/stations/city/:city', async (req, res) => {
  try {
    const { city } = req.params;
    const response = await axios.get('https://api.gen-ai-poc.com/stations', {
      params: { city }
    });
    
    res.json(response.data);
  } catch (error) {
    console.error('Error fetching stations:', error);
    res.status(500).json({ error: 'Failed to fetch stations' });
  }
});

app.listen(3000, () => {
  console.log('Server running on port 3000');
});
```

## 🧪 Testing

### Health Check
Use the `/hello` endpoint as a health check:

```bash
curl https://api.gen-ai-poc.com/hello
```

### Stations Endpoint Testing
```bash
# Basic test
curl https://api.gen-ai-poc.com/stations

# Test with error handling
curl -f https://api.gen-ai-poc.com/stations || echo "Request failed"

# Test response time
curl -w "@curl-format.txt" -o /dev/null -s https://api.gen-ai-poc.com/stations
```

Create `curl-format.txt`:
```
     time_namelookup:  %{time_namelookup}\n
        time_connect:  %{time_connect}\n
     time_appconnect:  %{time_appconnect}\n
    time_pretransfer:  %{time_pretransfer}\n
       time_redirect:  %{time_redirect}\n
  time_starttransfer:  %{time_starttransfer}\n
                     ----------\n
          time_total:  %{time_total}\n
```

## 📊 Rate Limiting

Currently, no rate limiting is implemented. However, we reserve the right to implement rate limiting in the future.

## 🔄 CORS

Cross-Origin Resource Sharing (CORS) is enabled for all origins in development and will be configured appropriately for production.

## 📈 Monitoring

The API is monitored for:
- Response times
- Error rates
- Availability
- Usage patterns

## 🚀 Future Endpoints

We plan to add more endpoints in future versions:
- Train schedules and routes
- Booking management
- User authentication
- Real-time train tracking
- Station amenities and services

## 📞 Support

### Getting Help
- **Documentation**: This document and project README
- **Issues**: Open an issue in the GitHub repository
- **Email**: api-support@gen-ai-poc.com (coming soon)

### API Status
- **Status Page**: https://status.gen-ai-poc.com (coming soon)
- **Uptime**: Monitored 24/7
- **Maintenance**: Scheduled maintenance notifications

## 📄 Changelog

### v1.0.0 (Current)
- Initial API release
- Hello endpoint
- Stations endpoint with comprehensive station data
- Basic error handling
- JSON response format
- Input validation and logging

### Upcoming
- Authentication system
- Rate limiting
- Train schedules endpoint
- Booking management endpoints
- WebSocket support for real-time updates

## 🔗 Related Links

- [Project Repository](https://github.com/your-org/gen-ai-poc)
- [Developer Portal](https://developers.gen-ai-poc.com) (coming soon)
- [API Status](https://status.gen-ai-poc.com) (coming soon)

---

**Last Updated:** June 2025  
**API Version:** v1.0.0  
**Documentation Version:** 1.1 