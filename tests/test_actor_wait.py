"""
This module contains unit tests for wait interactions.
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

import pytest

from screenplay.actor.actor import Actor
from screenplay.pattern import *
from screenplay.wait import wait, on, wait_on_question


# ------------------------------------------------------------------------------
# Fixtures
# ------------------------------------------------------------------------------

@pytest.fixture
def actor():
  a = Actor()
  a.knows(wait, wait_on_question)
  return a


# ------------------------------------------------------------------------------
# Pattern Functions
# ------------------------------------------------------------------------------

@question
def always_one():
  return 1


@question
def same_value(value):
  return value


# ------------------------------------------------------------------------------
# Tests for Wait Interactions
# ------------------------------------------------------------------------------

def test_wait_with_default_args(actor):
  wait_actor = wait(actor)
  assert wait_actor.traits['timeout'] == 30
  assert wait_actor.traits['interval'] == 1


def test_wait_with_explicit_args(actor):
  wait_actor = wait(actor, timeout=15, interval=0)
  assert wait_actor.traits['timeout'] == 15
  assert wait_actor.traits['interval'] == 0


def test_on_without_args(actor):
  on_actor = on(actor, always_one)
  assert on_actor.traits['on_question'] == always_one
  assert len(on_actor.traits['on_question_args']) == 0


def test_on_with_args(actor):
  on_actor = on(actor, same_value, value='stuff')
  assert on_actor.traits['on_question'] == same_value
  assert on_actor.traits['on_question_args'] == {'value': 'stuff'}


# to: condition without args
# to: condition with args
# to: non-condition
# to: non-question
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
