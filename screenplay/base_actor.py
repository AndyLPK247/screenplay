import functools
import inspect
import sys

from collections import OrderedDict
from screenplay.pattern import *


# TODO: Reconsider interaction *args?


# Base Screenplay Actor

class BaseActor:
  def __init__(self):
    self._abilities = OrderedDict()
    self._interactions = OrderedDict()
    self._sayings = OrderedDict()
    self._traits = OrderedDict()

  def _add_actor_context(self, actor):
    self._abilities.update(actor.abilities)
    self._interactions.update(actor.interactions)
    self._sayings.update(actor.sayings)
    self._traits.update(actor.traits)
  
  def _add_module_members(self, module):
    members = inspect.getmembers(module)
    self._get_members(members, is_ability, self._abilities)
    self._get_members(members, is_interaction, self._interactions)
    self._get_members(members, is_saying, self._sayings)

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
        self._add_module_members(arg)
      elif isinstance(arg, BaseActor):
        self._add_actor_context(arg)
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


class NotActorError(Exception):
  def __init__(self, obj):
    super().__init__(f'The {obj} object is not an actor')
    self.obj = obj


class UnknowableArgumentError(Exception):
  def __init__(self, argument):
    super().__init__(f'"{argument}" is not a module or screenplay function')
    self.argument = argument


class UnknownSayingError(Exception):
  def __init__(self, saying_name):
    super().__init__(f'The actor does not know "{saying_name}"')
    self.saying_name = saying_name


# Validations

def validate_actor(actor):
  if not isinstance(actor, BaseActor):
    raise NotActorError(actor)
