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


class IsNotEqualTo(ValueCondition):
  def evaluate(self, actual):
    return actual != self.value


class IsTrue(Condition):
  def evaluate(self, actual):
    return actual


class IsFalse(Condition):
  def evaluate(self, actual):
    return not actual


# --------------------------------------------------------------------------------
# Conditions for Numerical Comparisons
# --------------------------------------------------------------------------------

class IsGreaterThan(ValueCondition):
  def evaluate(self, actual):
    return actual > self.value


class IsGreaterThanOrEqualTo(ValueCondition):
  def evaluate(self, actual):
    return actual >= self.value


class IsLessThan(ValueCondition):
  def evaluate(self, actual):
    return actual < self.value


class IsLessThanOrEqualTo(ValueCondition):
  def evaluate(self, actual):
    return actual <= self.value


# --------------------------------------------------------------------------------
# Conditions for Containment
# --------------------------------------------------------------------------------

class Contains(ValueCondition):
  def evaluate(self, actual):
    return self.value in actual


class DoesNotContain(ValueCondition):
  def evaluate(self, actual):
    return self.value not in actual
