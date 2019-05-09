import functools

from screenplay.base_actor import BaseActor
from screenplay.pattern import *


# Actor Sayings

@saying
def call_ability(actor, name):
  if name.startswith('can_'):
    ability_name = name[4:]
    if ability_name in actor.abilities:
      ability = actor.abilities[ability_name]
      return functools.partial(actor.can, ability)


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


# Pythonic Screenplay Actor

class Actor(BaseActor):
  def __init__(self):
    super().__init__()
    self.knows(call_ability, call_interaction, traditional_screenplay)
