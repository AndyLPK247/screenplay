"""
This module provides interactions and saying for waiting.
These allow the actor to wait for given conditions to be met.
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

import functools
import time

from screenplay.actor.actor import Actor
from screenplay.actor.sayings import call_interaction
from screenplay.pattern import *


# ------------------------------------------------------------------------------
# Wait Interactions
# ------------------------------------------------------------------------------

@interaction
def wait(actor, timeout=30, interval=1):
  wait_actor = Actor()
  wait_actor.knows(actor, call_interaction, on, on_question)
  wait_actor.knows(timeout=timeout, interval=interval)
  return wait_actor


@interaction
def on(actor, question, **q_args):
  validate_question(question)
  on_actor = Actor()
  on_actor.knows(actor, call_interaction, to, to_condition)
  on_actor.knows(on_question=question, on_question_args=q_args)
  return on_actor


@interaction
def to(actor, condition, **c_args):
  validate_condition(condition)

  timeout = actor.traits['timeout']
  interval = actor.traits['interval']
  question = actor.traits['on_question']
  q_args = actor.traits['on_question_args']

  end = time.monotonic() + timeout
  answer = actor.call(question, **q_args)
  satisfied = actor.check(condition, actual=answer, **c_args)

  while not satisfied and time.monotonic() < end:
    time.sleep(interval)
    answer = actor.call(question, **q_args)
    satisfied = actor.check(condition, actual=answer, **c_args)

  if not satisfied:
    raise WaitTimeoutError(timeout, question, q_args, condition, c_args)


# ------------------------------------------------------------------------------
# Wait Sayings
# ------------------------------------------------------------------------------

@saying
def on_question(actor, name):
  if name.startswith('on_'):
    question_name = name[3:]
    if question_name in actor.interactions:
      question = actor.interactions[question_name]
      return functools.partial(actor.call, on, actor=actor, question=question)


@saying
def wait_on_question(actor, name):
  if name.startswith('wait_on_'):
    wait_actor = wait(actor)
    on_name = name[5:]
    return on_question(wait_actor, on_name)


@saying
def to_condition(actor, name):
  if name.startswith('to_'):
    condition_name = name[3:]
    if condition_name in actor.conditions:
      condition = actor.conditions[condition_name]
      return functools.partial(actor.call, to, actor=actor, condition=condition)


# ------------------------------------------------------------------------------
# Wait Exceptions
# ------------------------------------------------------------------------------

def _format_call(func, kwargs):
  name = func.__name__
  args = ", ".join([f"{k}={v}" for (k, v) in kwargs.items()])
  call = f'{name}({args})'
  return call


class WaitTimeoutError(Exception):
  def __init__(self, timeout, question, q_args, condition, c_args):
    q = _format_call(question, q_args)
    c = _format_call(condition, c_args)
    seconds = "seconds" if timeout != 1 else "second"
    super().__init__(f'Waiting for "{q}" to "{c}" timed out after {timeout} {seconds}')
    self.timeout = timeout
    self.question = question
    self.q_args = q_args
    self.condition = condition
    self.c_args = c_args
