import functools
import inspect

from screenplay.interactions import *


# TODO: errors for invalid args?
# TODO: add *args for actor interaction calls?
# TODO: add **kwargs for actor interaction calls?

# def interaction(a=1, b=2)
# def interaction(**kwargs)
# def interaction(a=1, b=2, **kwargs)


class Actor:
  def __init__(self):
    self._abilities = dict()
    self._interactions = dict()
    self._traits = dict()
  
  def _get_applicable_args(self, interaction, arg_dict):
    # Every parameter for the interaction must have either:
    #  (a) an value passed in
    #  (b) an ability
    #  (b) a default value

    applicable_args = dict()
    params = inspect.signature(interaction).parameters

    for name, param in params.items():
      if name in arg_dict:
        applicable_args[name] = arg_dict[name]
      elif name in self._traits:
        applicable_args[name] = self._traits[name]
      elif param.default == inspect.Parameter.empty:
        raise MissingParameterError(name, interaction)
    
    return applicable_args

  def knows(self, *args):
    for module in args:
      if not inspect.ismodule(module):
        raise NotModuleError(module)
      else:
        members = inspect.getmembers(module)
        abilities = {name: f for name, f in members if is_ability(f)}
        self._abilities.update(abilities)
        interactions = {name: f for name, f in members if is_interaction(f)}
        self._interactions.update(interactions)

  @property
  def traits(self):
    return self._traits

  def give_traits(self, **kwargs):
    # TODO: validation for duplicates
    self._traits.update(kwargs)

  def can(self, ability, *args, **kwargs):
    validate_ability(ability)
    traits = ability(*args, **kwargs)
    self.give_traits(**traits)

  def call(self, interaction, **kwargs):
    validate_interaction(interaction)
    applicable_args = self._get_applicable_args(interaction, kwargs)
    return interaction(**applicable_args)

  def attempts_to(self, task, **kwargs):
    validate_task(task)
    return self.call(task, **kwargs)

  def asks_for(self, question, **kwargs):
    validate_question(question)
    return self.call(question, **kwargs)

  def __getattr__(self, attr):
    # Try to get it as an ability
    if attr.startswith('can_'):
      ability_name = attr[4:]
      if ability_name not in self._abilities:
        raise UnknownAbilityError(ability_name)
      else:
        ability = self._abilities[ability_name]
        return functools.partial(self.can, ability)

    # Fall back to get it as an interaction
    else:
      if attr not in self._interactions:
        raise UnknownInteractionError(attr)
      else:
        interaction = self._interactions[attr]
        return functools.partial(self.call, interaction)


class MissingParameterError(Exception):
  def __init__(self, parameter, interaction):
    super().__init__(f'Parameter "{parameter}" is missing for {interaction.__name__}')
    self.parameter = parameter
    self.interaction = interaction


class NotModuleError(Exception):
  def __init__(self, module):
    super().__init__(f'"{module}" is not a module')
    self.module = module


class UnknownAbilityError(Exception):
  def __init__(self, ability_name):
    super().__init__(f'The actor does not know "{ability_name}"')
    self.ability_name = ability_name


class UnknownInteractionError(Exception):
  def __init__(self, interaction_name):
    super().__init__(f'The actor does not know "{interaction_name}"')
    self.interaction_name = interaction_name
