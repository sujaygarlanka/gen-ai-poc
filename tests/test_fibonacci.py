"""
Tests for the Fibonacci function module.
"""

import pytest
import sys
import os

# Add the src directory to the path so we can import the fibonacci module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from fibonacci import fibonacci_recursive, fibonacci_iterative, fibonacci_sequence


class TestFibonacciRecursive:
    """Test cases for the recursive Fibonacci implementation."""
    
    def test_fibonacci_recursive_base_cases(self):
        """Test base cases for recursive Fibonacci."""
        assert fibonacci_recursive(0) == 0
        assert fibonacci_recursive(1) == 1
    
    def test_fibonacci_recursive_small_numbers(self):
        """Test recursive Fibonacci for small numbers."""
        assert fibonacci_recursive(2) == 1
        assert fibonacci_recursive(3) == 2
        assert fibonacci_recursive(4) == 3
        assert fibonacci_recursive(5) == 5
        assert fibonacci_recursive(6) == 8
    
    def test_fibonacci_recursive_negative_input(self):
        """Test that recursive Fibonacci raises ValueError for negative input."""
        with pytest.raises(ValueError, match="Fibonacci sequence is not defined for negative numbers"):
            fibonacci_recursive(-1)


class TestFibonacciIterative:
    """Test cases for the iterative Fibonacci implementation."""
    
    def test_fibonacci_iterative_base_cases(self):
        """Test base cases for iterative Fibonacci."""
        assert fibonacci_iterative(0) == 0
        assert fibonacci_iterative(1) == 1
    
    def test_fibonacci_iterative_small_numbers(self):
        """Test iterative Fibonacci for small numbers."""
        assert fibonacci_iterative(2) == 1
        assert fibonacci_iterative(3) == 2
        assert fibonacci_iterative(4) == 3
        assert fibonacci_iterative(5) == 5
        assert fibonacci_iterative(6) == 8
        assert fibonacci_iterative(10) == 55
    
    def test_fibonacci_iterative_negative_input(self):
        """Test that iterative Fibonacci raises ValueError for negative input."""
        with pytest.raises(ValueError, match="Fibonacci sequence is not defined for negative numbers"):
            fibonacci_iterative(-1)
    
    def test_fibonacci_iterative_vs_recursive(self):
        """Test that iterative and recursive implementations give same results."""
        for i in range(15):  # Test up to 15 to avoid slow recursive calls
            assert fibonacci_iterative(i) == fibonacci_recursive(i)


class TestFibonacciSequence:
    """Test cases for the Fibonacci sequence generator."""
    
    def test_fibonacci_sequence_empty(self):
        """Test Fibonacci sequence with count 0."""
        assert fibonacci_sequence(0) == []
    
    def test_fibonacci_sequence_single(self):
        """Test Fibonacci sequence with count 1."""
        assert fibonacci_sequence(1) == [0]
    
    def test_fibonacci_sequence_small_counts(self):
        """Test Fibonacci sequence for small counts."""
        assert fibonacci_sequence(2) == [0, 1]
        assert fibonacci_sequence(5) == [0, 1, 1, 2, 3]
        assert fibonacci_sequence(8) == [0, 1, 1, 2, 3, 5, 8, 13]
    
    def test_fibonacci_sequence_negative_count(self):
        """Test that Fibonacci sequence raises ValueError for negative count."""
        with pytest.raises(ValueError, match="Count must be non-negative"):
            fibonacci_sequence(-1)
    
    def test_fibonacci_sequence_consistency(self):
        """Test that sequence values match individual function calls."""
        sequence = fibonacci_sequence(10)
        for i, value in enumerate(sequence):
            assert value == fibonacci_iterative(i)


if __name__ == "__main__":
    pytest.main([__file__])
