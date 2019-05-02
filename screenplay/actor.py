import functools
import inspect
import sys

from collections import OrderedDict
from screenplay.pattern import *


# Base Screenplay Actor

class BaseActor:
  def __init__(self):
    self._abilities = OrderedDict()
    self._interactions = OrderedDict()
    self._sayings = OrderedDict()
    self._traits = OrderedDict()

  def _get_args(self, interaction, arg_dict):
    applicable_args = dict()
    params = inspect.signature(interaction).parameters

    for name, param in params.items():
      if name in arg_dict:
        applicable_args[name] = arg_dict[name]
      elif name in self._traits:
        applicable_args[name] = self._traits[name]
      elif name == 'actor':
        applicable_args['actor'] = self
      elif param.default == inspect.Parameter.empty:
        raise MissingParameterError(name, interaction)
    
    return applicable_args

  def _get_members(self, members, predicate, target):
    for name, f in members:
      if predicate(f):
        target[name] = f

  @property
  def abilities(self):
    return self._abilities

  @property
  def interactions(self):
    return self._interactions

  @property
  def sayings(self):
    return self._sayings

  @property
  def traits(self):
    return self._traits

  def call(self, interaction, **kwargs):
    validate_interaction(interaction)
    applicable_args = self._get_args(interaction, kwargs)
    return interaction(**applicable_args)

  def can(self, ability, **kwargs):
    validate_ability(ability)
    traits = ability(**kwargs)
    self._traits.update(traits)

  def knows(self, *args, **kwargs):
    # TODO: validation for duplicates
    self._traits.update(kwargs)

    for arg in args:
      if inspect.ismodule(arg):
        members = inspect.getmembers(arg)
        self._get_members(members, is_ability, self._abilities)
        self._get_members(members, is_interaction, self._interactions)
        self._get_members(members, is_saying, self._sayings)
      elif is_ability(arg):
        self._abilities[arg.__name__] = arg
      elif is_interaction(arg):
        self._interactions[arg.__name__] = arg
      elif is_saying(arg):
        self._sayings[arg.__name__] = arg
      else:
        raise UnknowableArgumentError(arg)

  def __getattr__(self, attr):
    for name, saying in self._sayings.items():
      call = saying(self, attr)
      if call is not None:
        return call
    raise UnknownSayingError(attr)


# Actor Exceptions

class MissingParameterError(Exception):
  def __init__(self, parameter, interaction):
    super().__init__(f'Parameter "{parameter}" is missing for {interaction.__name__}')
    self.parameter = parameter
    self.interaction = interaction


class UnknowableArgumentError(Exception):
  def __init__(self, argument):
    super().__init__(f'"{argument}" is not a module or screenplay function')
    self.argument = argument


class UnknownSayingError(Exception):
  def __init__(self, saying_name):
    super().__init__(f'The actor does not know "{saying_name}"')
    self.saying_name = saying_name


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
