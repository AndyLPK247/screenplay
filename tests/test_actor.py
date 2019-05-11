"""
This module contains unit tests for the Actor class.
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

import pytest

from collections import OrderedDict
from screenplay.actor import Actor
from screenplay.pattern import *


# ------------------------------------------------------------------------------
# Fixtures
# ------------------------------------------------------------------------------

@pytest.fixture
def actor():
  """Creates an Actor instance with an empty context."""
  return Actor()


# ------------------------------------------------------------------------------
# Pattern Functions
# ------------------------------------------------------------------------------

@ability
def be_cool():
  return {'cool': True}


@ability
def go_super_saiyan():
  return {'hair': 'blonde', 'power': 9001}


@condition
def be(actual, value):
  return actual == value


@condition
def contain(actual, value):
  return value in actual


# ------------------------------------------------------------------------------
# Tests for Knowing Traits
# ------------------------------------------------------------------------------

@pytest.mark.parametrize(
  "attr",
  ['abilities', 'conditions', 'interactions', 'sayings', 'traits'])
def test_initial_actor_is_empty(actor, attr):
  attr_dict = getattr(actor, attr)
  assert isinstance(attr_dict, OrderedDict)
  assert len(attr_dict) == 0


@pytest.mark.parametrize(
  "key,value",
  [
    ("number", 3.14),
    ("string", "Hello, World!"),
    ("boolean", False),
    ("list", [1, 2, 3]),
    ("set", {1, 2, 3}),
    ("dict", {'a': 1, 'b': 2}),
    ("object", object())
  ]
)
def test_actor_knows_a_trait(actor, key, value):
  traits = {key: value}
  actor.knows(**traits)
  assert len(actor.traits) == 1
  assert actor.traits[key] == value


def test_actor_knows_multiple_traits_with_one_call_each(actor):
  actor.knows(a=1)
  actor.knows(b=2)
  actor.knows(c=3)
  assert len(actor.traits) == 3
  assert actor.traits['a'] == 1
  assert actor.traits['b'] == 2
  assert actor.traits['c'] == 3


def test_actor_knows_multiple_traits_with_one_call_for_all(actor):
  actor.knows(a=1, b=2, c=3)
  assert len(actor.traits) == 3
  assert actor.traits['a'] == 1
  assert actor.traits['b'] == 2
  assert actor.traits['c'] == 3


def test_actor_knows_traits_in_order(actor):
  actor.knows(e=5, d=4, c=3, b=2, a=1)
  assert list(actor.traits.keys()) == ['e', 'd', 'c', 'b', 'a']


def test_actor_knows_traits_being_overridden(actor):
  actor.knows(a=1, b=2, c=3)
  actor.knows(b=99)
  assert actor.traits['b'] == 99


# ------------------------------------------------------------------------------
# Tests for Knowing Abilities
# ------------------------------------------------------------------------------

def test_actor_knows_an_ability(actor):
  actor.knows(be_cool)
  assert len(actor.abilities) == 1
  assert actor.abilities['be_cool'] == be_cool


def test_actor_knows_multiple_abilities_with_one_call_each(actor):
  actor.knows(be_cool)
  actor.knows(go_super_saiyan)
  assert len(actor.abilities) == 2
  assert actor.abilities['be_cool'] == be_cool
  assert actor.abilities['go_super_saiyan'] == go_super_saiyan


def test_actor_knows_multiple_abilities_with_one_call_for_all(actor):
  actor.knows(be_cool, go_super_saiyan)
  assert len(actor.abilities) == 2
  assert actor.abilities['be_cool'] == be_cool
  assert actor.abilities['go_super_saiyan'] == go_super_saiyan


def test_actor_knows_abilities_in_order(actor):
  actor.knows(go_super_saiyan, be_cool)
  assert list(actor.abilities.keys()) == ['go_super_saiyan', 'be_cool']


# ------------------------------------------------------------------------------
# Tests for Knowing Conditions
# ------------------------------------------------------------------------------

def test_actor_knows_a_condition(actor):
  actor.knows(be)
  assert len(actor.conditions) == 1
  assert actor.conditions['be'] == be


def test_actor_knows_multiple_conditions_with_one_call_each(actor):
  actor.knows(be)
  actor.knows(contain)
  assert len(actor.conditions) == 2
  assert actor.conditions['be'] == be
  assert actor.conditions['contain'] == contain


def test_actor_knows_multiple_conditions_with_one_call_for_all(actor):
  actor.knows(be, contain)
  assert len(actor.conditions) == 2
  assert actor.conditions['be'] == be
  assert actor.conditions['contain'] == contain


def test_actor_knows_conditions_in_order(actor):
  actor.knows(contain, be)
  assert list(actor.conditions.keys()) == ['contain', 'be']


# Test Actor

# know interactions
# know sayings
# know actor
# know module
# know multiple
# know duplicate
# know none of the above
# can ability without args
# can ability with args
# can unknown ability
# can non-ability
# can duplicate traits
# call interaction without parameters
# call interaction without args and no traits
# call interaction with args and no traits
# call interaction without args and with traits
# call interaction with some args and traits
# call interaction with unnecessary traits
# call interaction with unnecessary args
# call interaction with missing parameters
# call interaction with actor parameter
# can unknown interaction
# call non-interaction
# getattr no sayings
# getattr match saying
# getattr unmatched saying
# getattr match first of multiple sayings


# Test Sayings

# call_ability: "can_" success
# call_ability: "can_" DNE
# call_interaction: success without parameters
# call_interaction: success with args only
# call_interaction: success with args and traits
# call_interaction: success with extra args
# call_interaction: DNE
# attempts_to: task
# attempts_to: interaction
# attempts_to: raw function
# asks_for: question
# asks_for: interaction
# asks_for: raw function


# Test Wait Interactions

# wait: defaults
# wait: arg values
# on: question without args
# on: question with args
# on: non-question
# to: condition without args
# to: condition with args
# to: non-condition
# to: success with no need to wait
# to: success after waiting
# to: no success after waiting (explicit timeout and interval)
# chain: actor.attempts_to(wait, timeout=30, interval=1).on(question, **).to(condition, **)
# chain: actor.attempts_to(wait, timeout=30, interval=1).on(question).to(condition)
# chain: actor.wait(timeout=30, interval=1).on(question).to(question)
# chain: actor.wait().on(question).to(question)


# Test Pythonic Wait Interactions

# on_question: success without parameters
# on_question: success with args only
# on_question: success with args and traits
# on_question: success with extra args
# on_question: DNE
# wait_on_question: success
# wait_on_question: DNE
# to_condition: success without parameters
# to_condition: success with args only
# to_condition: success with args and traits
# to_condition: success with extra args
# to_condition: DNE

# actor.wait().on_question().to_condition()
# actor.wait_on_question().to_condition()
# actor.wait_on_something(locator=SOME_ELEMENT).to_be(value=789)


# Future Tests?

# actor.wait_on_something(locator=SOME_ELEMENT).to_be(789)
# actor.wait_on_something(locator=SOME_ELEMENT).to_match("regex")
# actor.wait_on_something(locator=SOME_ELEMENT).to_contain_substring("substring")
# actor.wait_on_something(locator=SOME_ELEMENT).to_contain("a", "b", "c")
