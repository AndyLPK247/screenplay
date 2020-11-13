"""
Contains unit tests for the screenplay.wait module.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

import pytest
import time

from screenplay.conditions import IsEqualTo, IsGreaterThan, IsLessThan
from screenplay.core import Actor, Task, Question
from screenplay.waiting import WaitUntil, WaitingException


# ------------------------------------------------------------------------------
# Globals
# ------------------------------------------------------------------------------

COUNTER = 0


# ------------------------------------------------------------------------------
# Fixtures
# ------------------------------------------------------------------------------

@pytest.fixture
def actor():
  # Reset the counter
  global COUNTER
  COUNTER = 0

  # Construct the actor
  return Actor()


# ------------------------------------------------------------------------------
# Question for Testing
# ------------------------------------------------------------------------------

class NextCount(Question):
  def request_as(self, actor):
    global COUNTER
    COUNTER += 1
    return COUNTER


# ------------------------------------------------------------------------------
# Waiting Tests
# ------------------------------------------------------------------------------

def test_waiting_with_no_need_to_wait(actor, mocker):
  mocker.patch('time.sleep')
  answer = actor.attempts_to(WaitUntil(NextCount(), IsGreaterThan(0), timeout=1))
  time.sleep.assert_not_called()   # pylint: disable=no-member

  global COUNTER
  assert COUNTER == 1
  assert answer == 1


def test_waiting_successfully(actor, mocker):
  mocker.patch('time.sleep')
  answer = actor.attempts_to(WaitUntil(NextCount(), IsEqualTo(10), timeout=1))
  time.sleep.assert_called_with(0)   # pylint: disable=no-member

  global COUNTER
  assert COUNTER == 10
  assert answer == 10


def test_waiting_successfully_with_explicit_interval(actor, mocker):
  mocker.patch('time.sleep')
  answer = actor.attempts_to(WaitUntil(NextCount(), IsEqualTo(5), timeout=1, interval=0.01))
  time.sleep.assert_called_with(0.01)   # pylint: disable=no-member

  global COUNTER
  assert COUNTER == 5
  assert answer == 5


def test_waiting_failure(actor, mocker):
  mocker.patch('time.sleep')
  with pytest.raises(WaitingException): 
    actor.attempts_to(WaitUntil(NextCount(), IsLessThan(0), timeout=0.1, interval=0.01))

  global COUNTER
  assert COUNTER > 0
