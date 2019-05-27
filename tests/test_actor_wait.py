"""
This module contains unit tests for wait interactions.
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

import pytest
import time

from screenplay.actor.actor import Actor
from screenplay.pattern import *
from screenplay.wait import *


# ------------------------------------------------------------------------------
# Fixtures
# ------------------------------------------------------------------------------

@pytest.fixture
def actor():
  # Reset the counter
  global COUNTER
  COUNTER = 0

  # Construct the actor
  a = Actor()
  a.knows(wait, wait_on_question)
  return a


# ------------------------------------------------------------------------------
# Pattern Functions
# ------------------------------------------------------------------------------

COUNTER = 0

@question
def counter():
  global COUNTER
  COUNTER += 1
  return COUNTER


@question
def always_one():
  return 1


@question
def same_value(value):
  return value


@condition
def be(actual, value):
  return actual == value


# ------------------------------------------------------------------------------
# Tests for Wait Interaction Functions
# ------------------------------------------------------------------------------

def test_wait_function_with_default_args(actor):
  wait_actor = wait(actor)
  assert wait_actor.traits['timeout'] == 30
  assert wait_actor.traits['interval'] == 1


def test_wait_function_with_explicit_args(actor):
  wait_actor = wait(actor, timeout=15, interval=0)
  assert wait_actor.traits['timeout'] == 15
  assert wait_actor.traits['interval'] == 0


def test_on_function_without_args(actor):
  on_actor = on(actor, always_one)
  assert on_actor.traits['on_question'] == always_one
  assert len(on_actor.traits['on_question_args']) == 0


def test_on_function_with_args(actor):
  on_actor = on(actor, same_value, value='stuff')
  assert on_actor.traits['on_question'] == same_value
  assert on_actor.traits['on_question_args'] == {'value': 'stuff'}


def test_on_function_with_non_question(actor):
  with pytest.raises(NotQuestionError):
    on(actor, be)


def test_to_function_with_success_after_no_need_to_wait(actor, mocker):
  mocker.patch('time.sleep')
  wait_actor = wait(actor, timeout=1, interval=0.01)
  on_actor = on(wait_actor, always_one)
  to(on_actor, be, value=1)
  time.sleep.assert_not_called()


def test_to_function_with_success_after_waiting(actor, mocker):
  mocker.patch('time.sleep')
  wait_actor = wait(actor, timeout=1, interval=0)
  on_actor = on(wait_actor, counter)
  to(on_actor, be, value=10)
  time.sleep.assert_called_with(0)


def test_to_function_with_failure_after_waiting(actor):
  wait_actor = wait(actor, timeout=0.01, interval=0)
  on_actor = on(wait_actor, always_one)

  with pytest.raises(WaitTimeoutError):
    to(on_actor, be, value=2)


def test_to_function_with_non_condition(actor):
  wait_actor = wait(actor, timeout=0.01, interval=0)
  on_actor = on(wait_actor, always_one)

  with pytest.raises(NotConditionError):
    to(on_actor, always_one)


# ------------------------------------------------------------------------------
# Tests for Wait Interaction Chains
# ------------------------------------------------------------------------------

# def test_actor_call_wait_chain_with_args(actor):
#   # Expect no timeout exception
#   actor.knows(wait, call_interaction)
#   actor.wait(timeout=0.01, interval=0).on(question=counter).to(condition=be, value=5)


# def test_actor_call_wait_chain_with_traits(actor):
#   # Expect no timeout exception
#   actor.knows(timeout=0.01, interval=0, value=5)
#   actor.call(wait).on(counter).to(be)


# chain: actor.call(wait, timeout=30, interval=1).on(question, **).to(condition, **)
# chain: actor.call(wait, timeout=30, interval=1).on(question).to(condition)
# chain: actor.wait(timeout=30, interval=1).on(question).to(question)
# chain: actor.wait().on(question).to(question) with traits
# chain: actor.wait().on(question).to(question) with without traits


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
