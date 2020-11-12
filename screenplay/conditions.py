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
# Conditions for Equality
# --------------------------------------------------------------------------------

class IsEqualTo(Condition):

  def __init__(self, value):
    self.value = value

  def evaluate(self, actual):
    return actual == self.value


class IsNotEqualTo(IsEqualTo):

  def __init__(self, value):
    super().__init__(value)
  
  def evaluate(self, actual):
    return not super().evaluate(actual)


class IsTrue(IsEqualTo):

  def __init__(self):
    super().__init__(True)


class IsFalse(IsEqualTo):

  def __init__(self):
    super().__init__(False)


# --------------------------------------------------------------------------------
# Conditions for Numerical Comparisons
# --------------------------------------------------------------------------------

class IsGreaterThan(Condition):

  def __init__(self, value):
    self.value = value

  def evaluate(self, actual):
    return actual > self.value


class IsGreaterThanOrEqualTo(Condition):

  def __init__(self, value):
    self.value = value

  def evaluate(self, actual):
    return actual >= self.value


class IsLessThan(Condition):

  def __init__(self, value):
    self.value = value

  def evaluate(self, actual):
    return actual < self.value


class IsLessThanOrEqualTo(Condition):

  def __init__(self, value):
    self.value = value

  def evaluate(self, actual):
    return actual <= self.value


# --------------------------------------------------------------------------------
# Conditions for Containment
# --------------------------------------------------------------------------------

class Contains(Condition):

  def __init__(self, value):
    self.value = value

  def evaluate(self, actual):
    return self.value in actual


class DoesNotContain(Contains):

  def __init__(self, value):
    super().__init__(value)
  
  def evaluate(self, actual):
    return not super().evaluate(actual)
