import time

from screenplay.actor import call_interaction
from screenplay.base_actor import BaseActor, validate_actor
from screenplay.pattern import *


@interaction
def wait(actor, timeout, interval=1):
  validate_actor(actor)
  return WaitActor(actor, timeout, interval)


@interaction
def on(waiting_actor, question, **q_args):
  validate_question(question)
  return OnActor(waiting_actor, question, q_args)


@interaction
def to(on_actor, condition, **c_args):
  validate_condition(condition)

  timeout = on_actor.traits.timeout
  interval = on_actor.traits.timeout
  question = on_actor.traits.on_question
  q_args = on_actor.traits.on_question_args

  end = time.monotonic() + timeout
  answer = on_actor.call(question, **q_args)
  satisfied = condition(answer, **c_args)

  while not satisfied and time.monotonic() < end:
    time.sleep(interval)
    answer = on_actor.call(question, **q_args)
    satisfied = condition(answer, **c_args)

  if not satisfied:
    raise WaitTimeoutError(timeout, question, q_args, condition, c_args)


class WaitActor(BaseActor):
  def __init__(self, calling_actor, timeout, interval):
    super().__init__()
    self.knows(calling_actor, call_interaction, on)
    self.knows(timeout=timeout, interval=interval)


class OnActor(BaseActor):
  def __init__(self, wait_actor, question, question_args):
    super().__init__()
    self.knows(wait_actor, call_interaction, to)
    self.knows(on_question=question, on_question_args=question_args)


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


# wait(timeout=30, interval=1).on(existence, locator=SOME_ELEMENT).to(be, value=True)

# actor.attempts_to(wait, timeout=30, interval=1).on(existence, locator=SOME_ELEMENT).to(be, value=True)

# actor.wait(timeout=30, interval=1).on(something, locator=SOME_ELEMENT).to(be, value=789)
# actor.wait().on_something(locator=SOME_ELEMENT).to_be(value=789)
# actor.wait_on_something(locator=SOME_ELEMENT).to_be(value=789)

# actor.wait_on_something(locator=SOME_ELEMENT).to_be(789)
# actor.wait_on_something(locator=SOME_ELEMENT).to_match("regex")
# actor.wait_on_something(locator=SOME_ELEMENT).to_contain_substring("substring")
# actor.wait_on_something(locator=SOME_ELEMENT).to_contain("a", "b", "c")
