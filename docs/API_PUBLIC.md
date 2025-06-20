# Gen AI POC - Public API Documentation

Welcome to the Gen AI POC API documentation. This document provides comprehensive information for developers who want to integrate with our Flask API.

## 🌐 API Overview

The Gen AI POC API is a RESTful service built with Flask that provides simple, reliable endpoints for development and testing purposes.

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

#### Example Usage

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

**JavaScript (Async/Await)**
```javascript
async function getGreeting() {
  try {
    const response = await fetch('https://api.gen-ai-poc.com/hello');
    const data = await response.json();
    return data.message;
  } catch (error) {
    console.error('Error fetching greeting:', error);
    throw error;
  }
}
```

**Python (Requests)**
```python
import requests

def get_greeting():
    try:
        response = requests.get('https://api.gen-ai-poc.com/hello')
        response.raise_for_status()  # Raises an HTTPError for bad responses
        data = response.json()
        return data['message']
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

# Usage
greeting = get_greeting()
print(greeting)  # "Hello, world!"
```

**Python (aiohttp - Async)**
```python
import aiohttp
import asyncio

async def get_greeting_async():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.gen-ai-poc.com/hello') as response:
            if response.status == 200:
                data = await response.json()
                return data['message']
            else:
                raise Exception(f"HTTP {response.status}")

# Usage
greeting = asyncio.run(get_greeting_async())
print(greeting)
```

**cURL**
```bash
# Basic request
curl https://api.gen-ai-poc.com/hello

# With headers
curl -H "Accept: application/json" \
     -H "Content-Type: application/json" \
     https://api.gen-ai-poc.com/hello

# Verbose output
curl -v https://api.gen-ai-poc.com/hello
```

**Postman**
1. Create a new GET request
2. Set URL to: `https://api.gen-ai-poc.com/hello`
3. Send request
4. Response will be: `{"message": "Hello, world!"}`

## 🧪 Testing

### Health Check
Use the `/hello` endpoint as a health check:

```bash
curl https://api.gen-ai-poc.com/hello
```

Expected response:
```json
{
  "message": "Hello, world!"
}
```

### Testing Tools
- **Postman**: Import the API collection
- **Insomnia**: Use the provided examples
- **cURL**: Command-line testing
- **Browser**: Direct URL access

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
- User management
- Data processing
- File uploads
- Real-time notifications

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
- Basic error handling
- JSON response format

### Upcoming
- Authentication system
- Rate limiting
- Additional endpoints
- WebSocket support

## 🔗 Related Links

- [Project Repository](https://github.com/your-org/gen-ai-poc)
- [Developer Portal](https://developers.gen-ai-poc.com) (coming soon)
- [API Status](https://status.gen-ai-poc.com) (coming soon)

---

**Last Updated:** December 2024  
**API Version:** v1.0.0  
**Documentation Version:** 1.0 