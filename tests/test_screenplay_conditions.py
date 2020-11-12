"""
Contains unit tests for the screenplay.conditions module.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

from screenplay.conditions import *   # pylint: disable=unused-wildcard-import


# --------------------------------------------------------------------------------
# Tests for Equality Conditions
# --------------------------------------------------------------------------------

def test_IsEqualTo_true_for_numbers():
  assert IsEqualTo(3.14).evaluate(3.14)


def test_IsEqualTo_false_for_numbers():
  assert not IsEqualTo(3.14).evaluate(2.72)


def test_IsEqualTo_true_for_strings():
  assert IsEqualTo('hello').evaluate('hello')


def test_IsEqualTo_false_for_strings():
  assert not IsEqualTo('hello').evaluate('goodbye')


def test_IsNotEqualTo_true_for_numbers():
  assert not IsNotEqualTo(3.14).evaluate(3.14)


def test_IsNotEqualTo_false_for_numbers():
  assert IsNotEqualTo(3.14).evaluate(2.72)


def test_IsNotEqualTo_true_for_strings():
  assert not IsNotEqualTo('hello').evaluate('hello')


def test_IsNotEqualTo_false_for_strings():
  assert IsNotEqualTo('hello').evaluate('goodbye')


def test_IsTrue_true():
  assert IsTrue().evaluate(True)


def test_IsTrue_false():
  assert not IsTrue().evaluate(False)


def test_IsFalse_true():
  assert IsFalse().evaluate(False)


def test_IsFalse_false():
  assert not IsFalse().evaluate(True)


# --------------------------------------------------------------------------------
# Tests for Numerical Comparison Conditions
# --------------------------------------------------------------------------------

def test_IsGreaterThan_true():
  assert IsGreaterThan(100).evaluate(200)


def test_IsGreaterThan_false_when_less():
  assert not IsGreaterThan(100).evaluate(0)


def test_IsGreaterThan_false_when_equal():
  assert not IsGreaterThan(100).evaluate(100)


def test_IsGreaterThanOrEqualTo_true_when_greater():
  assert IsGreaterThanOrEqualTo(100).evaluate(200)


def test_IsGreaterThanOrEqualTo_true_when_equal():
  assert IsGreaterThanOrEqualTo(100).evaluate(100)


def test_IsGreaterThanOrEqualTo_false():
  assert not IsGreaterThanOrEqualTo(100).evaluate(0)


def test_IsLessThan_true():
  assert IsLessThan(100).evaluate(0)


def test_IsLessThan_false_when_greater():
  assert not IsLessThan(100).evaluate(200)


def test_IsLessThan_false_when_equal():
  assert not IsLessThan(100).evaluate(100)


def test_IsLessThanOrEqualTo_true_when_less():
  assert IsLessThanOrEqualTo(100).evaluate(0)


def test_IsLessThanOrEqualTo_true_when_equal():
  assert IsLessThanOrEqualTo(100).evaluate(100)


def test_IsLessThanOrEqualTo_false():
  assert not IsLessThanOrEqualTo(100).evaluate(200)


# --------------------------------------------------------------------------------
# Tests for Containment Conditions
# --------------------------------------------------------------------------------

def test_Contains_true_for_strings():
  assert Contains("lo").evaluate("Hello World!")
  

def test_Contains_false_for_strings():
  assert not Contains("bye").evaluate("Hello World!")


def test_Contains_true_for_lists():
  assert Contains("a").evaluate(["a", "b", "c"])


def test_Contains_false_for_lists():
  assert not Contains("d").evaluate(["a", "b", "c"])


def test_Contains_true_for_dicts():
  assert Contains("a").evaluate(dict(a=1, b=2, c=3))


def test_Contains_false_for_dicts():
  assert not Contains("d").evaluate(dict(a=1, b=2, c=3))


def test_DoesNotContain_true_for_strings():
  assert DoesNotContain("bye").evaluate("Hello World!")
  

def test_DoesNotContain_false_for_strings():
  assert not DoesNotContain("lo").evaluate("Hello World!")


def test_DoesNotContain_true_for_lists():
  assert DoesNotContain("d").evaluate(["a", "b", "c"])


def test_DoesNotContain_false_for_lists():
  assert not DoesNotContain("a").evaluate(["a", "b", "c"])


def test_DoesNotContain_true_for_dicts():
  assert DoesNotContain("d").evaluate(dict(a=1, b=2, c=3))


def test_DoesNotContain_false_for_dicts():
  assert not DoesNotContain("a").evaluate(dict(a=1, b=2, c=3))
