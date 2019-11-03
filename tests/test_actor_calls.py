"""
This module contains unit tests for Actor methods that call pattern functions.
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

import pytest
import sys

from screenplay.core.actor import Actor
from screenplay.core.exceptions import MissingParametersError, UnknownSayingError
from screenplay.core.interactions import interaction, condition, question, task, NotInteractionError


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
def do_nothing():
  return True


@interaction
def do_it(task, speed):
  return f"{task} at {speed} speed"


@condition
def equal(actual, value):
  return actual == value


@question
def always_true():
  return True


@question
def add_things(a=1, b=2):
  return a + b


@task
def whip_it_good():
  pass


def noop():
  pass


# ------------------------------------------------------------------------------
# Tests for Calling Interactions
# ------------------------------------------------------------------------------

def test_actor_calls_interaction_without_parameters(actor):
  response = actor.call(do_nothing)
  assert response


def test_actor_calls_interaction_with_args_and_without_traits(actor):
  response = actor.call(do_it, task="program", speed="lightning")
  assert response == "program at lightning speed"


def test_actor_calls_interaction_without_args_and_with_traits(actor):
  actor.knows(task="program", speed="lightning")
  response = actor.call(do_it)
  assert response == "program at lightning speed"


def test_actor_calls_interaction_with_both_args_and_traits(actor):
  actor.knows(task="program")
  response = actor.call(do_it, speed="lightning")
  assert response == "program at lightning speed"


def test_actor_calls_interaction_with_args_that_override_traits(actor):
  actor.knows(task="program", speed="lightning")
  response = actor.call(do_it, task="drive")
  assert response == "drive at lightning speed"


def test_actor_calls_interaction_with_unnecessary_args_that_are_ignored(actor):
  response = actor.call(do_it, task="program", speed="lightning", garbage=True)
  assert response == "program at lightning speed"


def test_actor_calls_interaction_with_unnecessary_traits_that_are_ignored(actor):
  actor.knows(garbage=True)
  response = actor.call(do_it, task="program", speed="lightning")
  assert response == "program at lightning speed"


def test_actor_calls_interaction_with_default_parameters(actor):
  response = actor.call(add_things)
  assert response == 3


def test_actor_calls_interaction_with_args_and_default_parameters(actor):
  response = actor.call(add_things, b=9)
  assert response == 10


def test_actor_calls_interaction_with_missing_parameters(actor):
  with pytest.raises(MissingParametersError):
    actor.call(do_it)


def test_actor_calls_interaction_with_an_actor_parameter(actor):
  @interaction
  def get_actor(actor):
    return actor
  
  response = actor.call(get_actor)
  assert response == actor


def test_actor_calls_interaction_with_variable_keyword_args(actor):
  @interaction
  def add_stuff(**kwargs):
    return kwargs['a'] + kwargs['b'] + kwargs['c']

  result = actor.call(add_stuff, a=1, b=2, c=3)
  assert result == 6


def test_actor_calls_interaction_with_positional_and_variable_keyword_args(actor):
  @interaction
  def add_stuff(first, second, **kwargs):
    return first + second + kwargs['a'] + kwargs['b'] + kwargs['c']

  result = actor.call(add_stuff, first=4, second=5, a=1, b=2, c=3)
  assert result == 15


def test_actor_calls_interaction_with_every_type_of_parameter(actor):
  @interaction
  def add_stuff(first, second, third=3, **kwargs):
    return first + second + third + kwargs['a'] + kwargs['b'] + kwargs['c']

  actor.knows(first=1)
  result = actor.call(add_stuff, second=2, a=4, b=5, c=6)
  assert result == 21


def test_actor_calls_a_non_interaction(actor):
  with pytest.raises(NotInteractionError):
    actor.call(noop)


# ------------------------------------------------------------------------------
# Tests for Calling Interactions with Sayings
# ------------------------------------------------------------------------------

def test_actor_calls_interaction_by_name_without_parameters(actor):
  actor.knows(do_nothing)
  response = actor.do_nothing()
  assert response


def test_actor_calls_interaction_by_name_with_args_and_without_traits(actor):
  actor.knows(do_it)
  response = actor.do_it(task="program", speed="lightning")
  assert response == "program at lightning speed"


def test_actor_calls_interaction_by_name_without_args_and_with_traits(actor):
  actor.knows(do_it, task="program", speed="lightning")
  response = actor.do_it()
  assert response == "program at lightning speed"


def test_actor_calls_interaction_by_name_with_both_args_and_traits(actor):
  actor.knows(do_it, task="program")
  response = actor.do_it(speed="lightning")
  assert response == "program at lightning speed"


def test_actor_calls_interaction_by_name_with_args_that_override_traits(actor):
  actor.knows(do_it, task="program", speed="lightning")
  response = actor.do_it(task="drive")
  assert response == "drive at lightning speed"


def test_actor_calls_interaction_by_name_with_unnecessary_args_that_are_ignored(actor):
  actor.knows(do_it)
  response = actor.do_it(task="program", speed="lightning", garbage=True)
  assert response == "program at lightning speed"


def test_actor_calls_interaction_by_name_with_unnecessary_traits_that_are_ignored(actor):
  actor.knows(do_it, garbage=True)
  response = actor.do_it(task="program", speed="lightning")
  assert response == "program at lightning speed"


def test_actor_calls_interaction_by_call_without_parameters(actor):
  actor.knows(do_nothing)
  response = actor.call_do_nothing()
  assert response


def test_actor_calls_interaction_by_call_with_args_and_without_traits(actor):
  actor.knows(do_it)
  response = actor.call_do_it(task="program", speed="lightning")
  assert response == "program at lightning speed"


def test_actor_calls_interaction_by_call_without_args_and_with_traits(actor):
  actor.knows(do_it, task="program", speed="lightning")
  response = actor.call_do_it()
  assert response == "program at lightning speed"


def test_actor_calls_interaction_by_call_with_both_args_and_traits(actor):
  actor.knows(do_it, task="program")
  response = actor.call_do_it(speed="lightning")
  assert response == "program at lightning speed"


def test_actor_calls_interaction_by_call_with_args_that_override_traits(actor):
  actor.knows(do_it, task="program", speed="lightning")
  response = actor.call_do_it(task="drive")
  assert response == "drive at lightning speed"


def test_actor_calls_interaction_by_call_with_unnecessary_args_that_are_ignored(actor):
  actor.knows(do_it)
  response = actor.call_do_it(task="program", speed="lightning", garbage=True)
  assert response == "program at lightning speed"


def test_actor_calls_interaction_by_call_with_unnecessary_traits_that_are_ignored(actor):
  actor.knows(do_it, garbage=True)
  response = actor.call_do_it(task="program", speed="lightning")
  assert response == "program at lightning speed"


# ------------------------------------------------------------------------------
# Tests for Calling Other Interaction Types with Sayings
# ------------------------------------------------------------------------------

@pytest.mark.parametrize(
  "callname",
  ["equal", "call_equal", "check_equal", "asks_for_equal"])
def test_actor_calls_condition_by_saying(actor, callname):
  actor.knows(equal)
  response = getattr(actor, callname)(actual="a", value="b")
  assert not response


@pytest.mark.parametrize(
  "callname",
  ["add_things", "call_add_things", "get_add_things", "asks_for_add_things"])
def test_actor_calls_question_by_saying(actor, callname):
  actor.knows(add_things)
  response = getattr(actor, callname)(a=5, b=9)
  assert response == 14


@pytest.mark.parametrize(
  "callname",
  ["whip_it_good", "call_whip_it_good", "do_whip_it_good", "attempts_to_whip_it_good"])
def test_actor_calls_task_by_saying(actor, callname):
  actor.knows(whip_it_good)
  response = getattr(actor, callname)()
  assert response is None
