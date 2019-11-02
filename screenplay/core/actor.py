"""
This module contains the base Actor class.
Actor is the main "actor" in the Screenplay pattern.
Pattern functions (like interactions) are in other modules.
"""

# TODO: first argument in a call chain?
# TODO: *args for callables?
# TODO: class for fluent extensions?

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

import functools
import inspect

from collections import OrderedDict
from screenplay.core.exceptions import *
from screenplay.core.pattern import *


# ------------------------------------------------------------------------------
# Screenplay Actor Class
# ------------------------------------------------------------------------------

class Actor:
  def __init__(self, *args, **kwargs):
    self._abilities = OrderedDict()
    self._conditions = OrderedDict()
    self._interactions = OrderedDict()
    self._sayings = OrderedDict()
    self._traits = OrderedDict()

    self.knows(*args, **kwargs)

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
    params = inspect.signature(function).parameters
    full_context = self._get_full_context(arg_dict)

    kwargs = {n: p for n, p in params.items()
              if p.kind == inspect.Parameter.VAR_KEYWORD}
    
    missing = {n: p for n, p in params.items()
               if n not in full_context
               and p.kind != inspect.Parameter.VAR_POSITIONAL
               and p.kind != inspect.Parameter.VAR_KEYWORD
               and p.default == inspect.Parameter.empty}

    if len(missing) > 0:
      raise MissingParametersError(function, missing.keys())
    elif len(kwargs) > 0:
      applicable_args = full_context
    else:
      applicable_args = {n: p for n, p in full_context.items() if n in params}

    return applicable_args

  def _get_full_context(self, arg_dict):
    full_context = {'actor': self}
    full_context.update(self._traits)
    full_context.update(arg_dict)
    return full_context

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
