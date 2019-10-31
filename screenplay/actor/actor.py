"""
This module contains the base Actor class.
Actor is the main "actor" in the Screenplay pattern.
Pattern functions (like interactions) are in other modules.
"""

# TODO: *args for callables?
# TODO: class for fluent extensions?

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

import functools
import inspect

from collections import OrderedDict
from screenplay.actor.exceptions import *
from screenplay.pattern import *


# ------------------------------------------------------------------------------
# Screenplay Actor Class
# ------------------------------------------------------------------------------

class Actor:
  def __init__(self):
    self._abilities = OrderedDict()
    self._conditions = OrderedDict()
    self._interactions = OrderedDict()
    self._sayings = OrderedDict()
    self._traits = OrderedDict()

  def _add_actor_context(self, actor):
    self._abilities.update(actor.abilities)
    self._conditions.update(actor.conditions)
    self._interactions.update(actor.interactions)
    self._sayings.update(actor.sayings)
    self._traits.update(actor.traits)
  
  def _add_module_members(self, module):
    members = inspect.getmembers(module)
    self._get_members(members, is_ability, self._abilities)
    self._get_members(members, is_condition, self._conditions)
    self._get_members(members, is_interaction, self._interactions)
    self._get_members(members, is_saying, self._sayings)

  def _get_args(self, function, arg_dict):
    applicable_args = dict()
    params = inspect.signature(function).parameters

    for name, param in params.items():
      if name in arg_dict:
        applicable_args[name] = arg_dict[name]
      elif name in self._traits:
        applicable_args[name] = self._traits[name]
      elif name == 'actor':
        applicable_args['actor'] = self
      elif param.default == inspect.Parameter.empty:
        raise MissingParameterError(name, function)
    
    return applicable_args

  def _get_members(self, members, predicate, target):
    for name, f in members:
      if predicate(f):
        target[name] = f

  @property
  def abilities(self):
    return self._abilities

  @property
  def conditions(self):
    return self._conditions

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

  def check(self, condition, **kwargs):
    validate_condition(condition)
    applicable_args = self._get_args(condition, kwargs)
    return condition(**applicable_args)

  def knows(self, *args, **kwargs):
    self._traits.update(kwargs)

    for arg in args:
      if inspect.ismodule(arg):
        self._add_module_members(arg)
      elif isinstance(arg, Actor):
        self._add_actor_context(arg)
      elif is_ability(arg):
        self._abilities[arg.__name__] = arg
      elif is_condition(arg):
        self._conditions[arg.__name__] = arg
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
