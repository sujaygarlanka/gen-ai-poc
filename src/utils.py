"""
Utility functions for the Gen AI POC application.
"""

def format_response_data(data, title="Data Response"):
    """
    Format API response data for consistent output.
    
    Args:
        data (dict or list): The data to format
        title (str): Title for the formatted response
        
    Returns:
        dict: Formatted response with metadata
    """
    return {
        "title": title,
        "data": data,
        "timestamp": __import__('datetime').datetime.now().isoformat(),
        "status": "success"
    }


def validate_api_response(response):
    """
    Validate API response and extract data safely.
    
    Args:
        response: HTTP response object
        
    Returns:
        dict: Validated response data or error information
    """
    try:
        if response.status_code == 200:
            return {
                "success": True,
                "data": response.json()
            }
        else:
            return {
                "success": False,
                "error": f"API request failed with status {response.status_code}",
                "data": None
            }
    except Exception as e:
        return {
            "success": False,
            "error": f"Error processing response: {str(e)}",
            "data": None
        }


def calculate_percentage_change(old_value, new_value):
    """
    Calculate percentage change between two values.
    
    Args:
        old_value (float): Original value
        new_value (float): New value
        
    Returns:
        float: Percentage change (positive for increase, negative for decrease)
    """
    if old_value == 0:
        return float('inf') if new_value > 0 else 0
    
    return ((new_value - old_value) / old_value) * 100
