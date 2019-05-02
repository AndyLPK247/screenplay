import time
from screenplay.pattern import *


# TODO: default timeout?


@interaction
def wait_for(interaction, timeout, interval=0, **kwargs):
  validate_interaction(interaction)
  # TODO: how will kwargs get passed to here from the actor?
  return WaitExecutor(interaction, kwargs, timeout, interval=interval)


# TODO: @condition?
# TODO: rename interaction module to pattern?
# TODO: partial interaction with kwargs?


def be(value):
  return lambda actual: actual == value


class WaitExecutor:
  def __init__(self, interaction, arg_dict, timeout, interval=0):
    self.interaction = interaction
    self.arg_dict = arg_dict
    self.timeout = timeout
    self.interval = interval
  
  def to(self, condition, **kwargs):
    # end = time.monotonic() + self.timeout
    # time.sleep(self.interval)
    pass

  def __getattr__(self, attr):
    pass


# wait_for(existence, locator=SOME_ELEMENT).to(be, value=True)

# actor.attempts_to(wait_for, question=existence, locator=SOME_ELEMENT).to(be, value=True)

# actor.wait_for(existence, locator=SOME_ELEMENT, condition=to_be, value_to_be=False)
# actor.wait_for_existence(locator=SOME_ELEMENT, condition=to_be, value_to_be=False)
# actor.wait_for_existence(locator=SOME_ELEMENT).to_be(False)

# actor.wait_for_something(locator=SOME_ELEMENT).to(be, value=789)

# actor.wait_for_something(locator=SOME_ELEMENT).to_be(789)
# actor.wait_for_something(locator=SOME_ELEMENT).to_match("regex")
# actor.wait_for_something(locator=SOME_ELEMENT).to_contain_substring("substring")
# actor.wait_for_something(locator=SOME_ELEMENT).to_contain("a", "b", "c")
