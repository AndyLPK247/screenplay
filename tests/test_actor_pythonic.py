"""
This module contains unit tests for Pythonic sayings for Screenplay Actors.
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

import pytest

from screenplay.actor.builders import init_actor
from screenplay.actor.exceptions import MissingParameterError, UnknownSayingError
from screenplay.pattern import *


# ------------------------------------------------------------------------------
# Fixtures
# ------------------------------------------------------------------------------

@pytest.fixture
def pythonic_actor():
  """Creates an Actor instance with the full Pythonic context."""
  return init_actor()


# ------------------------------------------------------------------------------
# Pattern Functions
# ------------------------------------------------------------------------------

@ability
def be_cool():
  return {'cool': True}


@ability
def go_super_saiyan(extra):
  return {'hair': 'blonde', 'power': 9001, 'extra': extra}


@interaction
def do_it(task, speed):
  return f"{task} at {speed} speed"


@interaction
def whip_it_good():
  return True


@interaction
def assume_things(a=1, b=2):
  return a + b


def noop():
  pass


# ------------------------------------------------------------------------------
# Tests for Calling Abilities via "can_" Sayings
# ------------------------------------------------------------------------------

def test_actor_can_do_ability_without_args_via_saying(pythonic_actor):
  pythonic_actor.knows(be_cool)
  pythonic_actor.can_be_cool()
  assert len(pythonic_actor.traits) == 1
  assert pythonic_actor.traits['cool'] == True


def test_actor_can_do_ability_with_args_via_saying(pythonic_actor):
  pythonic_actor.knows(go_super_saiyan)
  pythonic_actor.can_go_super_saiyan(extra='yes')
  assert len(pythonic_actor.traits) == 3
  assert pythonic_actor.traits['hair'] == 'blonde'
  assert pythonic_actor.traits['power'] == 9001
  assert pythonic_actor.traits['extra'] == 'yes'


def test_actor_cannot_do_unknown_ability_via_saying(pythonic_actor):
  pythonic_actor.knows(go_super_saiyan)
  with pytest.raises(UnknownSayingError):
    pythonic_actor.can_be_cool()


def test_actor_cannot_do_non_ability_via_saying(pythonic_actor):
  with pytest.raises(UnknownSayingError):
    pythonic_actor.can_noop()


# ------------------------------------------------------------------------------
# Tests for Calling Interactions via Direct Sayings
# ------------------------------------------------------------------------------

def test_actor_calls_interaction_without_parameters_via_saying(pythonic_actor):
  pythonic_actor.knows(whip_it_good)
  response = pythonic_actor.whip_it_good()
  assert response


def test_actor_calls_interaction_with_args_and_without_traits_via_saying(pythonic_actor):
  pythonic_actor.knows(do_it)
  response = pythonic_actor.do_it(task="program", speed="lightning")
  assert response == "program at lightning speed"


def test_actor_calls_interaction_without_args_and_with_traits_via_saying(pythonic_actor):
  pythonic_actor.knows(do_it)
  pythonic_actor.knows(task="program", speed="lightning")
  response = pythonic_actor.do_it()
  assert response == "program at lightning speed"


def test_actor_calls_interaction_with_both_args_and_traits_via_saying(pythonic_actor):
  pythonic_actor.knows(do_it)
  pythonic_actor.knows(task="program")
  response = pythonic_actor.do_it(speed="lightning")
  assert response == "program at lightning speed"


def test_actor_calls_interaction_with_args_that_override_traits_via_saying(pythonic_actor):
  pythonic_actor.knows(do_it)
  pythonic_actor.knows(task="program", speed="lightning")
  response = pythonic_actor.do_it(task="drive")
  assert response == "drive at lightning speed"


def test_actor_calls_interaction_with_unnecessary_args_that_are_ignored_via_saying(pythonic_actor):
  pythonic_actor.knows(do_it)
  response = pythonic_actor.do_it(task="program", speed="lightning", garbage=True)
  assert response == "program at lightning speed"


def test_actor_calls_interaction_with_unnecessary_traits_that_are_ignored_via_saying(pythonic_actor):
  pythonic_actor.knows(do_it)
  pythonic_actor.knows(garbage=True)
  response = pythonic_actor.do_it(task="program", speed="lightning")
  assert response == "program at lightning speed"


def test_actor_calls_interaction_with_default_parameters_via_saying(pythonic_actor):
  pythonic_actor.knows(assume_things)
  response = pythonic_actor.assume_things()
  assert response == 3


def test_actor_calls_interaction_with_args_and_default_parameters_via_saying(pythonic_actor):
  pythonic_actor.knows(assume_things)
  response = pythonic_actor.assume_things(b=9)
  assert response == 10


def test_actor_calls_interaction_with_missing_parameters_via_saying(pythonic_actor):
  pythonic_actor.knows(do_it)
  with pytest.raises(MissingParameterError):
    pythonic_actor.do_it()


def test_actor_calls_interaction_with_an_actor_parameter_via_saying(pythonic_actor):
  @interaction
  def get_actor(actor):
    return actor
  
  pythonic_actor.knows(get_actor)
  response = pythonic_actor.get_actor()
  assert response == pythonic_actor


def test_actor_calls_a_non_interaction_via_saying(pythonic_actor):
  with pytest.raises(UnknownSayingError):
    pythonic_actor.noop()


# ------------------------------------------------------------------------------
# Tests for Asking Questions via "get_"
# ------------------------------------------------------------------------------

def test_actor_gets_an_answer_to_a_question_via_saying(pythonic_actor):
  @question
  def greeting(name):
    return f'Hello, {name}!'

  pythonic_actor.knows(greeting)
  response = pythonic_actor.get_greeting(name='Andy')
  assert response == 'Hello, Andy!'


def test_actor_asks_a_non_question_via_saying(pythonic_actor):
  with pytest.raises(UnknownSayingError):
    pythonic_actor.get_noop()


# ------------------------------------------------------------------------------
# Tests for Calling Tasks via "attempts_to"
# ------------------------------------------------------------------------------

def test_actor_attempts_to_do_a_task(pythonic_actor):
  saved = 0

  @task
  def do_stuff(value):
    nonlocal saved
    saved = value

  pythonic_actor.attempts_to(do_stuff, value = 1)
  assert saved == 1


def test_actor_attempts_to_do_an_interaction(pythonic_actor):
  with pytest.raises(NotTaskError):
    pythonic_actor.attempts_to(do_it)


def test_actor_attempts_to_do_a_raw_function(pythonic_actor):
  with pytest.raises(NotTaskError):
    pythonic_actor.attempts_to(noop)


# ------------------------------------------------------------------------------
# Tests for Calling Questions via "asks_for"
# ------------------------------------------------------------------------------

def test_actor_asks_for_a_question(pythonic_actor):
  @question
  def some_info(value):
    return value
  
  answer = pythonic_actor.asks_for(some_info, value=True)
  assert answer


def test_actor_asks_for_an_interaction(pythonic_actor):
  with pytest.raises(NotQuestionError):
    pythonic_actor.asks_for(do_it)


def test_actor_asks_for_a_raw_function(pythonic_actor):
  with pytest.raises(NotQuestionError):
    pythonic_actor.asks_for(noop)
