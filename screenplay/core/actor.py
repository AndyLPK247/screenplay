"""
This module contains the base Actor class.
Actor is the main "actor" in the Screenplay pattern.
Pattern functions (like interactions) are in other modules.
"""

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
    self._sayings = OrderedDict()
    self._traits = OrderedDict()
    self.knows(*args, **kwargs)

  def _add_actor_context(self, actor):
    self._sayings.update(actor.sayings)
    self._traits.update(actor.traits)
  
  def _add_interaction(self, interaction):
    for saying in interaction.sayings:
      if saying not in self._sayings:
        part = functools.partial(self.call, interaction)
        functools.update_wrapper(part, interaction)
        self._sayings[saying] = part
      else:
        raise DuplicateSayingError(saying, interaction)

  def _add_module_members(self, module):
    members = inspect.getmembers(module)
    for _, f in members:
      if is_interaction(f):
        self._add_interaction(f)

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

  def knows(self, *args, **kwargs):
    self._traits.update(kwargs)

    for arg in args:
      if inspect.ismodule(arg):
        self._add_module_members(arg)
      elif isinstance(arg, Actor):
        self._add_actor_context(arg)
      elif is_interaction(arg):
        self._add_interaction(arg)
      else:
        raise UnknowableArgumentError(arg)

  def __getattr__(self, attr):
    if attr in self._sayings:
      return self._sayings[attr]
    else:
      raise UnknownSayingError(attr)
