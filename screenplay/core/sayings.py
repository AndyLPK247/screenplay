"""
This module provides Pythonic sayings for actors.
The standard 'init_actor' builder automatically adds them to the constructed actor.
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

import functools

from screenplay.core.pattern import *


# ------------------------------------------------------------------------------
# Pythonic Sayings
# ------------------------------------------------------------------------------

@saying
def ask_question(actor, name):
  if name.startswith('get_'):
    question_name = name[4:]
    if question_name in actor.interactions:
      interaction = actor.interactions[question_name]
      if is_question(interaction):
        return functools.partial(actor.call, interaction)


@saying
def call_interaction(actor, name):
  if name in actor.interactions:
    interaction = actor.interactions[name]
    return functools.partial(actor.call, interaction)


@saying
def traditional_screenplay(actor, name):
  if name == 'attempts_to':
    def attempts_to(task, **kwargs):
      validate_task(task)
      return actor.call(task, **kwargs)
    return attempts_to
  elif name == 'asks_for':
    def asks_for(question, **kwargs):
      validate_question(question)
      return actor.call(question, **kwargs)
    return asks_for
