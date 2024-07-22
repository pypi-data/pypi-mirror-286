import operator
from unittest.mock import Mock
from desimpy.distributions import (
    Distribution, 
    dist_cast, 
    TransformDistribution,
    DegenerateDistribution
    )

# Concrete Distribution subclass for testing
class ConcreteDistribution(Distribution):
    def sample(self, context=None):
        return 1

def test_distribution_repr():
    dist = ConcreteDistribution()
    assert repr(dist) == "ConcreteDistribution"

def test_distribution_addition():
    dist1 = ConcreteDistribution()
    dist2 = ConcreteDistribution()
    result = dist1 + dist2
    assert isinstance(result, TransformDistribution)
    assert result.operation == operator.add

def test_distribution_subtraction():
    dist1 = ConcreteDistribution()
    dist2 = ConcreteDistribution()
    result = dist1 - dist2
    assert isinstance(result, TransformDistribution)
    assert result.operation == operator.sub

def test_distribution_multiplication():
    dist1 = ConcreteDistribution()
    dist2 = ConcreteDistribution()
    result = dist1 * dist2
    assert isinstance(result, TransformDistribution)
    assert result.operation == operator.mul

def test_distribution_division():
    dist1 = ConcreteDistribution()
    dist2 = ConcreteDistribution()
    result = dist1 / dist2
    assert isinstance(result, TransformDistribution)
    assert result.operation == operator.truediv

def test_transform_distribution_sample():
    dist1 = ConcreteDistribution()
    dist2 = ConcreteDistribution()
    transform_dist = TransformDistribution((dist1, dist2), operator.add)
    assert transform_dist.sample() == 2

def test_dist_cast_with_distribution():
    dist = ConcreteDistribution()
    assert dist_cast(dist) == dist

def test_dist_cast_with_invalid_type():
    with pytest.raises(TypeError):
        dist_cast(5)

def test_dist_cast_with_number():
    obj = 5
    result = dist_cast(obj)
    assert isinstance(result, DegenerateDistribution)
    assert result.sample() == 5

def test_dist_cast_with_distribution():
    obj = ConcreteDistribution()
    result = dist_cast(obj)
    assert result == obj

def test_dist_cast_with_callable():
    obj = lambda context: 10
    result = dist_cast(obj)
    assert isinstance(result, DegenerateDistribution)
    assert result.sample() == 10

def test_dist_cast_with_string():
    obj = "test_string"
    result = dist_cast(obj)
    assert isinstance(result, DegenerateDistribution)
    assert result.sample() == "test_string"

def test_dist_cast_with_invalid_type():
    obj = [1, 2, 3]
    with pytest.raises(ValueError):
        dist_cast(obj)
