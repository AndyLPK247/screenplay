"""
This module contains unit tests for the Actor class.
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

import pytest
import sys

from collections import OrderedDict
from screenplay.actor import Actor, UnknowableArgumentError
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
def go_super_saiyan(extra):
  return {'hair': 'blonde', 'power': 9001, 'extra': extra}


@condition
def be(actual, value):
  return actual == value


@condition
def contain(actual, value):
  return value in actual


@interaction
def do_it(task):
  return f"{task} is done"


@interaction
def whip_it_good():
  pass


@question
def some_question():
  pass


@saying
def try_things(actor, name):
  def try_it():
    return f"tried {name}"
  return try_it


@saying
def shout(actor, name):
  def out_loud(words):
    return words.upper()
  return out_loud


@task
def some_task():
  pass


# ------------------------------------------------------------------------------
# Pattern Assertion Functions
# ------------------------------------------------------------------------------

def assert_abilities(actor):
  assert len(actor.abilities) == 2
  assert actor.abilities['be_cool'] == be_cool
  assert actor.abilities['go_super_saiyan'] == go_super_saiyan


def assert_conditions(actor):
  assert len(actor.conditions) == 2
  assert actor.conditions['be'] == be
  assert actor.conditions['contain'] == contain


def assert_interactions(actor, include_tq=False):
  if include_tq:
    assert len(actor.interactions) == 4
    assert actor.interactions['some_task'] == some_task
    assert actor.interactions['some_question'] == some_question
  else:
    assert len(actor.interactions) == 2

  assert actor.interactions['do_it'] == do_it
  assert actor.interactions['whip_it_good'] == whip_it_good


def assert_sayings(actor):
  assert len(actor.sayings) == 2
  assert actor.sayings['try_things'] == try_things
  assert actor.sayings['shout'] == shout


def assert_all_functions(actor, include_tq=False):
  assert_abilities(actor)
  assert_conditions(actor)
  assert_interactions(actor, include_tq=include_tq)
  assert_sayings(actor)


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
  assert_abilities(actor)


def test_actor_knows_multiple_abilities_with_one_call_for_all(actor):
  actor.knows(be_cool, go_super_saiyan)
  assert_abilities(actor)


def test_actor_knows_abilities_in_order(actor):
  actor.knows(go_super_saiyan, be_cool)
  assert list(actor.abilities.keys()) == ['go_super_saiyan', 'be_cool']


def test_actor_knows_a_duplicate_ability(actor):
  actor.knows(be_cool, go_super_saiyan)
  actor.knows(be_cool)
  assert_abilities(actor)


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
  assert_conditions(actor)


def test_actor_knows_multiple_conditions_with_one_call_for_all(actor):
  actor.knows(be, contain)
  assert_conditions(actor)


def test_actor_knows_conditions_in_order(actor):
  actor.knows(contain, be)
  assert list(actor.conditions.keys()) == ['contain', 'be']


def test_actor_knows_a_duplicate_condition(actor):
  actor.knows(be, contain)
  actor.knows(be)
  assert_conditions(actor)


# ------------------------------------------------------------------------------
# Tests for Knowing Interactions
# ------------------------------------------------------------------------------

def test_actor_knows_an_interaction(actor):
  actor.knows(do_it)
  assert len(actor.interactions) == 1
  assert actor.interactions['do_it'] == do_it


def test_actor_knows_a_task(actor):
  actor.knows(some_task)
  assert len(actor.interactions) == 1
  assert actor.interactions['some_task'] == some_task


def test_actor_knows_a_question(actor):
  actor.knows(some_question)
  assert len(actor.interactions) == 1
  assert actor.interactions['some_question'] == some_question


def test_actor_knows_multiple_interactions_with_one_call_each(actor):
  actor.knows(do_it)
  actor.knows(whip_it_good)
  assert_interactions(actor)


def test_actor_knows_multiple_interactions_with_one_call_for_all(actor):
  actor.knows(do_it, whip_it_good)
  assert_interactions(actor)


def test_actor_knows_interactions_in_order(actor):
  actor.knows(whip_it_good, do_it)
  assert list(actor.interactions.keys()) == ['whip_it_good', 'do_it']


def test_actor_knows_a_duplicate_interaction(actor):
  actor.knows(do_it, whip_it_good)
  actor.knows(do_it)
  assert_interactions(actor)


# ------------------------------------------------------------------------------
# Tests for Knowing Sayings
# ------------------------------------------------------------------------------

def test_actor_knows_a_saying(actor):
  actor.knows(try_things)
  assert len(actor.sayings) == 1
  assert actor.sayings['try_things'] == try_things


def test_actor_knows_multiple_sayings_with_one_call_each(actor):
  actor.knows(try_things)
  actor.knows(shout)
  assert_sayings(actor)


def test_actor_knows_multiple_sayings_with_one_call_for_all(actor):
  actor.knows(try_things, shout)
  assert_sayings(actor)


def test_actor_knows_sayings_in_order(actor):
  actor.knows(shout, try_things)
  assert list(actor.sayings.keys()) == ['shout', 'try_things']


def test_actor_knows_a_duplicate_saying(actor):
  actor.knows(try_things, shout)
  actor.knows(try_things)
  assert_sayings(actor)


# ------------------------------------------------------------------------------
# Tests for Knowing Multiple Types
# ------------------------------------------------------------------------------

def test_actor_knows_multiple_types_with_one_call(actor):
  actor.knows(be_cool, go_super_saiyan, be, contain, do_it, whip_it_good, try_things, shout)
  assert_all_functions(actor)


# ------------------------------------------------------------------------------
# Tests for Knowing Modules
# ------------------------------------------------------------------------------

def test_actor_knows_module(actor):
  actor.knows(sys.modules[__name__])
  assert_all_functions(actor, include_tq=True)


# ------------------------------------------------------------------------------
# Tests for Knowing Other Actors
# ------------------------------------------------------------------------------

def test_actor_knows_another_actor(actor):
  other = Actor()
  other.knows(be_cool, go_super_saiyan, be, contain, do_it, whip_it_good, try_things, shout)
  actor.knows(other)
  assert_all_functions(actor)


# ------------------------------------------------------------------------------
# Tests for Attempting to Know Non-Screenplay Items
# ------------------------------------------------------------------------------

def test_actor_cannot_know_an_arbitrary_function(actor):
  def func():
    pass

  with pytest.raises(UnknowableArgumentError):
    actor.knows(func)


def test_actor_cannot_know_an_arbitrary_object(actor):
  obj = object()
  with pytest.raises(UnknowableArgumentError):
    actor.knows(obj)


def test_actor_cannot_know_an_arbitrary_list(actor):
  stuff = list((1, 2, 3))
  with pytest.raises(UnknowableArgumentError):
    actor.knows(stuff)


def test_actor_cannot_know_an_arbitrary_set(actor):
  stuff = set((1, 2, 3))
  with pytest.raises(UnknowableArgumentError):
    actor.knows(stuff)


def test_actor_cannot_know_an_arbitrary_dict(actor):
  stuff = dict(a=1, b=2, c=3)
  with pytest.raises(UnknowableArgumentError):
    actor.knows(stuff)


# ------------------------------------------------------------------------------
# Tests for Having Abilities
# ------------------------------------------------------------------------------

def test_actor_can_do_ability_without_args(actor):
  actor.can(be_cool)
  assert len(actor.traits) == 1
  assert actor.traits['cool'] == True


def test_actor_can_do_ability_with_args(actor):
  actor.can(go_super_saiyan, extra='yes')
  assert len(actor.traits) == 3
  assert actor.traits['hair'] == 'blonde'
  assert actor.traits['power'] == 9001
  assert actor.traits['extra'] == 'yes'


def test_actor_cannot_do_non_ability(actor):
  def noop():
    pass
  
  with pytest.raises(NotAbilityError):
    actor.can(noop)


# Test Actor

# call interaction without parameters
# call interaction without args and no traits
# call interaction with args and no traits
# call interaction without args and with traits
# call interaction with some args and traits
# call interaction with unnecessary traits
# call interaction with unnecessary args
# call interaction with missing parameters
# call interaction with actor parameter
# call unknown interaction
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
