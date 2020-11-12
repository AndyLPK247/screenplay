"""
Contains support for waiting for interactions.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

import time

from screenplay.core import Task, ScreenplayException


# --------------------------------------------------------------------------------
# Class: wait_until
# --------------------------------------------------------------------------------

class WaitUntil(Task):

  def __init__(self, question, condition, timeout=30, interval=0):
    self.question = question
    self.condition = condition
    self.timeout = timeout
    self.interval = interval

  def perform_as(self, actor):
    end = time.monotonic() + self.timeout
    answer = actor.asks_for(self.question)
    satisfied = self.condition.evaluate(answer)

    while not satisfied and time.monotonic() < end:
      time.sleep(self.interval)
      answer = actor.asks_for(self.question)
      satisfied = self.condition.evaluate(answer)

    if not satisfied:
      raise WaitingException(actor, self.question, self.condition, self.timeout)

    return answer


# --------------------------------------------------------------------------------
# Class: WaitingException
# --------------------------------------------------------------------------------

class WaitingException(ScreenplayException):
  def __init__(self, actor, question, condition, timeout):
    super().__init__(f'The actor "{actor}" failed to wait until "{question}" "{condition}" for {timeout}s')
    self.actor = actor
    self.question = question
    self.condition = condition
    self.timeout = timeout
