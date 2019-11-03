"""
This module contains unit tests for the Actor class's 'knows' method.
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

import pytest
import sys

from collections import OrderedDict
from screenplay.core.actor import Actor
from screenplay.core.exceptions import DuplicateSayingError, UnknowableArgumentError
from screenplay.core.interactions import interaction, condition, question, task


# ------------------------------------------------------------------------------
# Fixtures
# ------------------------------------------------------------------------------

@pytest.fixture
def actor():
  """Creates an Actor instance with an empty context."""
  return Actor()


# ------------------------------------------------------------------------------
# Interaction Functions
# ------------------------------------------------------------------------------

@interaction
def do_it(task, speed):
  return f"{task} at {speed} speed"


@condition
def equal(actual, value):
  return actual == value


@question
def answer():
  return "answered"


@task
def some_task():
  pass


def noop():
  pass


# ------------------------------------------------------------------------------
# Saying Assertion Functions
# ------------------------------------------------------------------------------

def assert_do_it(actor):
  assert actor.sayings['do_it'].__name__ == do_it.__name__
  assert actor.sayings['call_do_it'].__name__ == do_it.__name__


def assert_equal(actor):
  assert actor.sayings['equal'].__name__ == equal.__name__
  assert actor.sayings['call_equal'].__name__ == equal.__name__
  assert actor.sayings['check_equal'].__name__ == equal.__name__
  assert actor.sayings['asks_for_equal'].__name__ == equal.__name__


def assert_answer(actor):
  assert actor.sayings['answer'].__name__ == answer.__name__
  assert actor.sayings['call_answer'].__name__ == answer.__name__
  assert actor.sayings['get_answer'].__name__ == answer.__name__
  assert actor.sayings['asks_for_answer'].__name__ == answer.__name__


def assert_some_task(actor):
  assert actor.sayings['some_task'].__name__ == some_task.__name__
  assert actor.sayings['call_some_task'].__name__ == some_task.__name__
  assert actor.sayings['do_some_task'].__name__ == some_task.__name__
  assert actor.sayings['attempts_to_some_task'].__name__ == some_task.__name__


def assert_all_sayings(actor):
  assert len(actor.sayings) == 14
  assert_do_it(actor)
  assert_equal(actor)
  assert_answer(actor)
  assert_some_task(actor)


# ------------------------------------------------------------------------------
# Tests for Knowing Traits
# ------------------------------------------------------------------------------

@pytest.mark.parametrize("attr", ['sayings', 'traits'])
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
# Tests for Knowing Interactions
# ------------------------------------------------------------------------------

def test_actor_knows_an_interaction(actor):
  actor.knows(do_it)
  assert len(actor.sayings) == 2
  assert_do_it(actor)


def test_actor_knows_a_condition(actor):
  actor.knows(equal)
  assert len(actor.sayings) == 4
  assert_equal(actor)


def test_actor_knows_a_question(actor):
  actor.knows(answer)
  assert len(actor.sayings) == 4
  assert_answer(actor)


def test_actor_knows_a_task(actor):
  actor.knows(some_task)
  assert len(actor.sayings) == 4
  assert_some_task(actor)


def test_actor_knows_multiple_interactions_with_one_call_each(actor):
  actor.knows(do_it)
  actor.knows(equal)
  actor.knows(answer)
  actor.knows(some_task)
  assert_all_sayings(actor)


def test_actor_knows_multiple_interactions_with_one_call_for_all(actor):
  actor.knows(do_it, equal, answer, some_task)
  assert_all_sayings(actor)


def test_actor_knows_interactions_in_order(actor):
  actor.knows(do_it, equal, answer, some_task)
  assert list(actor.sayings.keys()) == [
    'do_it',
    'call_do_it',
    'equal',
    'call_equal',
    'check_equal',
    'asks_for_equal',
    'answer',
    'call_answer',
    'get_answer',
    'asks_for_answer',
    'some_task',
    'call_some_task',
    'do_some_task',
    'attempts_to_some_task',
  ]


def test_actor_knows_a_duplicate_interaction(actor):
  actor.knows(do_it, equal)
  with pytest.raises(DuplicateSayingError):
    actor.knows(do_it)


# ------------------------------------------------------------------------------
# Tests for Knowing Modules
# ------------------------------------------------------------------------------

def test_actor_knows_module(actor):
  actor.knows(sys.modules[__name__])
  assert_all_sayings(actor)


# ------------------------------------------------------------------------------
# Tests for Knowing Other Actors
# ------------------------------------------------------------------------------

def test_actor_knows_another_actor(actor):
  other = Actor()
  other.knows(do_it, equal, answer, some_task)
  actor.knows(other)
  assert_all_sayings(actor)


# ------------------------------------------------------------------------------
# Tests for Attempting to Know Non-Screenplay Items
# ------------------------------------------------------------------------------

def test_actor_cannot_know_an_arbitrary_function(actor):
  with pytest.raises(UnknowableArgumentError):
    actor.knows(noop)


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
# Tests for Knowing Items via Initialization
# ------------------------------------------------------------------------------

def test_initial_actor_knows_traits():
  actor = Actor(a=1, b=2)
  assert len(actor.traits) == 2
  assert actor.traits['a'] == 1
  assert actor.traits['b'] == 2


def test_initial_actor_knows_interaction():
  actor = Actor(do_it)
  assert len(actor.sayings) == 2
  assert_do_it(actor)


def test_initial_actor_knows_condition():
  actor = Actor(equal)
  assert len(actor.sayings) == 4
  assert_equal(actor)


def test_initial_actor_knows_question():
  actor = Actor(answer)
  assert len(actor.sayings) == 4
  assert_answer(actor)


def test_initial_actor_knows_task():
  actor = Actor(some_task)
  assert len(actor.sayings) == 4
  assert_some_task(actor)


def test_initial_actor_knows_multiple_interactions():
  actor = Actor(do_it, equal, answer, some_task)
  assert_all_sayings(actor)


def test_initial_actor_knows_module(actor):
  actor = Actor(sys.modules[__name__])
  assert_all_sayings(actor)


def test_initial_actor_knows_another_actor(actor):
  other = Actor()
  other.knows(do_it, equal, answer, some_task)
  actor = Actor(other)
  assert_all_sayings(actor)


def test_initial_actor_cannot_know_an_arbitrary_function(actor):
  with pytest.raises(UnknowableArgumentError):
    Actor(noop)
