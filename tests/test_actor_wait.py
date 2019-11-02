"""
This module contains unit tests for wait interactions.
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

import pytest
import time

from screenplay.core.actor import Actor, UnknownSayingError
from screenplay.core.pattern import *
from screenplay.core.wait import *


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
  a.knows(call_interaction, wait, wait_on_question)
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
def multi_counter(inc=2):
  global COUNTER
  COUNTER += inc
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
  global COUNTER
  assert COUNTER == 10


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

def test_actor_call_wait_chain_with_args(actor, mocker):
  mocker.patch('time.sleep')
  actor.call(wait, timeout=0.01, interval=0).on(question=counter).to(condition=be, value=5)
  time.sleep.assert_called_with(0)
  global COUNTER
  assert COUNTER == 5


def test_actor_call_wait_chain_with_traits(actor, mocker):
  mocker.patch('time.sleep')
  actor.knows(timeout=0.01, interval=0, value=5)
  actor.call(wait).on(question=counter).to(condition=be)
  time.sleep.assert_called_with(0)
  global COUNTER
  assert COUNTER == 5


def test_actor_wait_chain_with_args_and_traits(actor, mocker):
  mocker.patch('time.sleep')
  actor.knows(timeout=0.01, interval=0)
  actor.wait().on(question=counter, inc=5).to(condition=be, value=10)
  time.sleep.assert_called_with(0)
  global COUNTER
  assert COUNTER == 10


def test_actor_wait_chain_with_failure(actor):
  with pytest.raises(WaitTimeoutError):
    actor.knows(timeout=0.01, interval=0)
    actor.wait().on(question=always_one).to(condition=be, value=2)


# ------------------------------------------------------------------------------
# Test Pythonic Wait Interactions
# ------------------------------------------------------------------------------

def test_actor_on_question_success_without_parameters(actor, mocker):
  mocker.patch('time.sleep')
  actor.knows(counter, timeout=0.01, interval=0)
  actor.wait().on_counter().to(condition=be, value=5)
  time.sleep.assert_called_with(0)
  global COUNTER
  assert COUNTER == 5


def test_actor_on_question_success_with_parameters(actor, mocker):
  mocker.patch('time.sleep')
  actor.knows(multi_counter, timeout=0.01, interval=0)
  actor.wait().on_multi_counter(inc=5).to(condition=be, value=10)
  time.sleep.assert_called_with(0)
  global COUNTER
  assert COUNTER == 10


def test_actor_on_question_success_with_traits(actor, mocker):
  mocker.patch('time.sleep')
  actor.knows(multi_counter, timeout=0.01, interval=0, inc=5, value=10)
  actor.wait().on_multi_counter().to(condition=be)
  time.sleep.assert_called_with(0)
  global COUNTER
  assert COUNTER == 10


def test_actor_on_question_success_with_extra_args(actor, mocker):
  mocker.patch('time.sleep')
  actor.knows(multi_counter, timeout=0.01, interval=0)
  actor.wait().on_multi_counter(inc=5, garbage="yup").to(condition=be, value=10)
  time.sleep.assert_called_with(0)
  global COUNTER
  assert COUNTER == 10


def test_actor_on_question_failure(actor):
  with pytest.raises(WaitTimeoutError):
    actor.knows(always_one, timeout=0.01, interval=0)
    actor.wait().on_always_one().to(condition=be, value=2)


def test_actor_on_question_dne(actor):
  with pytest.raises(UnknownSayingError):
    actor.wait(timeout=0.01, interval=0).on_counter()


# ------------------------------------------------------------------------------
# Test Pythonic Wait-On-Question Interactions
# ------------------------------------------------------------------------------

def test_actor_wait_on_question_success(actor, mocker):
  mocker.patch('time.sleep')
  actor.knows(multi_counter, timeout=0.01, interval=0)
  actor.wait_on_multi_counter(inc=5).to(condition=be, value=10)
  time.sleep.assert_called_with(0)
  global COUNTER
  assert COUNTER == 10


def test_actor_wait_on_question_failure(actor):
  with pytest.raises(WaitTimeoutError):
    actor.knows(always_one, timeout=0.01, interval=0)
    actor.wait_on_always_one().to(condition=be, value=2)


def test_actor_wait_on_question_dne(actor):
  with pytest.raises(UnknownSayingError):
    actor.knows(timeout=0.01, interval=0)
    actor.wait_on_counter()


# ------------------------------------------------------------------------------
# Test Pythonic Wait-On-Question-To-Condition Interactions
# ------------------------------------------------------------------------------

def test_actor_wait_on_question_to_condition_success(actor, mocker):
  mocker.patch('time.sleep')
  actor.knows(multi_counter, be, timeout=0.01, interval=0)
  actor.wait_on_multi_counter(inc=5).to_be(value=10)
  time.sleep.assert_called_with(0)
  global COUNTER
  assert COUNTER == 10


def test_actor_wait_on_question_to_condition_success_with_traits(actor, mocker):
  mocker.patch('time.sleep')
  actor.knows(multi_counter, be, timeout=0.01, interval=0, inc=5, value=10)
  actor.wait_on_multi_counter().to_be()
  time.sleep.assert_called_with(0)
  global COUNTER
  assert COUNTER == 10


def test_actor_wait_on_question_to_condition_failure(actor):
  with pytest.raises(WaitTimeoutError):
    actor.knows(always_one, be, timeout=0.01, interval=0)
    actor.wait_on_always_one().to_be(value=2)


def test_actor_wait_on_question_to_condition_dne(actor):
  with pytest.raises(UnknownSayingError):
    actor.knows(counter, timeout=0.01, interval=0)
    actor.wait_on_counter().to_be(value=2)
