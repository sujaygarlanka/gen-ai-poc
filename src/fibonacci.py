"""
Fibonacci function implementation.

This module provides functions to calculate Fibonacci numbers using different approaches.
"""


def fibonacci_recursive(n):
    """
    Calculate the nth Fibonacci number using recursion.
    
    Args:
        n (int): The position in the Fibonacci sequence (0-indexed)
        
    Returns:
        int: The nth Fibonacci number
        
    Raises:
        ValueError: If n is negative
    """
    if n < 0:
        raise ValueError("Fibonacci sequence is not defined for negative numbers")
    
    if n <= 1:
        return n
    
    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)


def fibonacci_iterative(n):
    """
    Calculate the nth Fibonacci number using iteration (more efficient).
    
    Args:
        n (int): The position in the Fibonacci sequence (0-indexed)
        
    Returns:
        int: The nth Fibonacci number
        
    Raises:
        ValueError: If n is negative
    """
    if n < 0:
        raise ValueError("Fibonacci sequence is not defined for negative numbers")
    
    if n <= 1:
        return n
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    
    return b


def fibonacci_sequence(count):
    """
    Generate a list of the first 'count' Fibonacci numbers.
    
    Args:
        count (int): Number of Fibonacci numbers to generate
        
    Returns:
        list: List of the first 'count' Fibonacci numbers
        
    Raises:
        ValueError: If count is negative
    """
    if count < 0:
        raise ValueError("Count must be non-negative")
    
    if count == 0:
        return []
    
    sequence = [0]
    if count > 1:
        sequence.append(1)
        
    for i in range(2, count):
        sequence.append(sequence[i-1] + sequence[i-2])
    
    return sequence


if __name__ == "__main__":
    # Example usage
    print("Fibonacci Examples:")
    print(f"fibonacci_recursive(10) = {fibonacci_recursive(10)}")
    print(f"fibonacci_iterative(10) = {fibonacci_iterative(10)}")
    print(f"fibonacci_sequence(10) = {fibonacci_sequence(10)}")
