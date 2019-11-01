"""
This module contains unit tests for Actor methods that call pattern functions.
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

import pytest
import sys

from screenplay.actor.actor import Actor
from screenplay.actor.exceptions import MissingParametersError, UnknownSayingError
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
def assume_bool(a=1, b=1):
  return a == b


@interaction
def do_it(task, speed):
  return f"{task} at {speed} speed"


@interaction
def whip_it_good():
  return True


@interaction
def assume_things(a=1, b=2):
  return a + b


@saying
def try_things(actor, name):
  if len(name) > 1:
    def try_it():
      return f"tried {name}"
    return try_it


@saying
def shout(actor, name):
  if name == "shout":
    def out_loud(words):
      return words.upper()
    return out_loud


def noop():
  pass


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
  with pytest.raises(NotAbilityError):
    actor.can(noop)


# ------------------------------------------------------------------------------
# Tests for Calling Interactions
# ------------------------------------------------------------------------------

def test_actor_calls_interaction_without_parameters(actor):
  response = actor.call(whip_it_good)
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
  response = actor.call(assume_things)
  assert response == 3


def test_actor_calls_interaction_with_args_and_default_parameters(actor):
  response = actor.call(assume_things, b=9)
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
# Tests for Checking Conditions
# ------------------------------------------------------------------------------

def test_actor_checks_condition_without_parameters_to_be_true(actor):
  @condition
  def always_true():
    return True
  
  response = actor.check(always_true)
  assert response == True


def test_actor_checks_condition_without_parameters_to_be_false(actor):
  @condition
  def always_false():
    return False
  
  response = actor.check(always_false)
  assert response == False


def test_actor_checks_condition_with_args_and_without_traits(actor):
  response = actor.check(be, actual=4, value=4)
  assert response == True


def test_actor_checks_condition_without_args_and_with_traits(actor):
  actor.knows(actual="hi", value="hi")
  response = actor.check(be)
  assert response == True


def test_actor_checks_condition_with_both_args_and_traits(actor):
  actor.knows(actual="hi")
  response = actor.check(be, value="hi")
  assert response == True


def test_actor_checks_condition_with_args_that_override_traits(actor):
  actor.knows(actual=99, value=99)
  response = actor.check(be, value=2)
  assert response == False


def test_actor_checks_condition_with_unnecessary_args_that_are_ignored(actor):
  response = actor.check(be, actual=4, value=4, garbage="bo-ha-ha")
  assert response == True


def test_actor_checks_condition_with_unnecessary_traits_that_are_ignored(actor):
  actor.knows(actual=99, value=99, garbage="stuff")
  response = actor.check(be)
  assert response == True


def test_actor_checks_condition_with_default_parameters(actor):
  response = actor.check(assume_bool)
  assert response == True


def test_actor_checks_condition_with_args_and_default_parameters(actor):
  response = actor.check(assume_bool, b=2)
  assert response == False


def test_actor_checks_condition_with_missing_parameters(actor):
  with pytest.raises(MissingParametersError):
    actor.check(be)


def test_actor_checks_condition_with_an_actor_parameter(actor):
  @condition
  def has_actor(actor):
    return actor is not None
  
  response = actor.check(has_actor)
  assert response == True


def test_actor_checks_a_non_condition(actor):
  with pytest.raises(NotConditionError):
    actor.check(noop)


# ------------------------------------------------------------------------------
# Tests for Calling Sayings
# ------------------------------------------------------------------------------

def test_actor_getattr_matches_saying(actor):
  actor.knows(shout)
  response = actor.shout("yay")
  assert response == "YAY"


def test_actor_getattr_matches_first_of_multiple_sayings(actor):
  actor.knows(shout, try_things)
  response = actor.shout("yay")
  assert response == "YAY"


def test_actor_getattr_does_not_match_saying(actor):
  actor.knows(shout, try_things)
  with pytest.raises(UnknownSayingError):
    actor.a("stuff")


def test_actor_getattr_does_not_have_sayings(actor):
  with pytest.raises(UnknownSayingError):
    actor.shout("yay")
