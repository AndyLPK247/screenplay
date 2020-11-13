"""
Contains basic conditions for waiting.
Implement new conditions by creating subclasses of Condition.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

from abc import ABC, abstractmethod


# --------------------------------------------------------------------------------
# Abstract Class: Condition
# --------------------------------------------------------------------------------

class Condition(ABC):
  @abstractmethod
  def evaluate(self, actual):
    pass


# --------------------------------------------------------------------------------
# Abstract Class: ValueCondition
# --------------------------------------------------------------------------------

class ValueCondition(ABC):
  def __init__(self, value):
    self.value = value


# --------------------------------------------------------------------------------
# Conditions for Equality
# --------------------------------------------------------------------------------

class IsEqualTo(ValueCondition):
  def evaluate(self, actual):
    return actual == self.value
  def __str__(self):
    return f'is equal to {self.value}'


class IsNotEqualTo(ValueCondition):
  def evaluate(self, actual):
    return actual != self.value
  def __str__(self):
    return f'is not equal to {self.value}'


class IsTrue(Condition):
  def evaluate(self, actual):
    return actual
  def __str__(self):
    return 'is True'


class IsFalse(Condition):
  def evaluate(self, actual):
    return not actual
  def __str__(self):
    return 'is False'


# --------------------------------------------------------------------------------
# Conditions for Numerical Comparisons
# --------------------------------------------------------------------------------

class IsGreaterThan(ValueCondition):
  def evaluate(self, actual):
    return actual > self.value
  def __str__(self):
    return f'is greater than {self.value}'


class IsGreaterThanOrEqualTo(ValueCondition):
  def evaluate(self, actual):
    return actual >= self.value
  def __str__(self):
    return f'is greater than or equal to {self.value}'


class IsLessThan(ValueCondition):
  def evaluate(self, actual):
    return actual < self.value
  def __str__(self):
    return f'is less than {self.value}'


class IsLessThanOrEqualTo(ValueCondition):
  def evaluate(self, actual):
    return actual <= self.value
  def __str__(self):
    return f'is less than or equal to {self.value}'


# --------------------------------------------------------------------------------
# Conditions for Containment
# --------------------------------------------------------------------------------

class Contains(ValueCondition):
  def evaluate(self, actual):
    return self.value in actual
  def __str__(self):
    return f'contains {self.value}'


class DoesNotContain(ValueCondition):
  def evaluate(self, actual):
    return self.value not in actual
  def __str__(self):
    return f'does not contain {self.value}'
