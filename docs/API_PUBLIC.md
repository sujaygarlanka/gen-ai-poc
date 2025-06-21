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

Retrieves a list of all available train stations with their details.

#### Request
```bash
curl -X GET https://api.gen-ai-poc.com/stations
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
async function getStations() {
  try {
    const response = await fetch('https://api.gen-ai-poc.com/stations');
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

// Usage
getStations();
```

**Python (Requests)**
```python
import requests

def get_stations():
    """Fetch all train stations."""
    try:
        response = requests.get('https://api.gen-ai-poc.com/stations')
        response.raise_for_status()
        stations = response.json()
        
        # Display stations
        for station in stations:
            print(f"{station['name']} ({station['code']}) - {station['city']}")
        
        return stations
    except requests.exceptions.RequestException as e:
        print(f"Error fetching stations: {e}")
        return []

def find_station_by_code(code):
    """Find a station by its code."""
    stations = get_stations()
    for station in stations:
        if station['code'].upper() == code.upper():
            return station
    return None

# Usage examples
stations = get_stations()
print(f"Total stations: {len(stations)}")

# Find specific station
nys_station = find_station_by_code('NYS')
if nys_station:
    print(f"Found: {nys_station['name']} in {nys_station['city']}")
```

**Python (aiohttp - Async)**
```python
import aiohttp
import asyncio

async def get_stations_async():
    """Asynchronously fetch all train stations."""
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get('https://api.gen-ai-poc.com/stations') as response:
                if response.status == 200:
                    stations = await response.json()
                    return stations
                else:
                    raise Exception(f"HTTP {response.status}")
        except Exception as e:
            print(f"Error: {e}")
            return []

# Usage
stations = asyncio.run(get_stations_async())
print(f"Retrieved {len(stations)} stations")
```

**cURL Examples**
```bash
# Get all stations
curl https://api.gen-ai-poc.com/stations

# Pretty print JSON response
curl https://api.gen-ai-poc.com/stations | python -m json.tool

# Save response to file
curl https://api.gen-ai-poc.com/stations -o stations.json

# Include response headers
curl -i https://api.gen-ai-poc.com/stations
```

**Node.js (Express Integration)**
```javascript
const express = require('express');
const axios = require('axios');
const app = express();

// Endpoint to get stations and format them
app.get('/api/formatted-stations', async (req, res) => {
  try {
    const response = await axios.get('https://api.gen-ai-poc.com/stations');
    const stations = response.data;
    
    // Format stations for frontend
    const formattedStations = stations.map(station => ({
      value: station.code,
      label: `${station.name} - ${station.city}`,
      city: station.city
    }));
    
    res.json(formattedStations);
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