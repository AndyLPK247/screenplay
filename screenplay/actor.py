import functools
import inspect

from screenplay.decorators import is_ability, is_interaction


class Actor:
  def __init__(self):
    self._abilities = dict()
    self._interactions = dict()
    self._traits = dict()
  
  def _can_do_ability(self, ability_name, *args, **kwargs):
    ability = self._abilities[ability_name]
    traits = ability(*args, **kwargs)
    self.can(**traits)

  def _get_applicable_args(self, func, **kwargs):
    # Every parameter for the callable must have either:
    #  (a) an value passed in
    #  (b) an ability
    #  (b) a default value

    applicable_args = dict()
    params = inspect.signature(func).parameters

    for name, param in params.items():
      if name in kwargs:
        applicable_args[name] = kwargs[name]
      elif name in self._traits:
        applicable_args[name] = self._traits[name]
      elif param.default == inspect.Parameter.empty:
        raise Exception(f"Parameter '{name}' is missing for {func.__name__}")
    
    return applicable_args

  def can(self, **kwargs):
    # TODO: validation
    self._traits.update(kwargs)

  def knows(self, *args):
    # TODO: validation
    for module in args:
      members = inspect.getmembers(module)

      abilities = {name: f for name, f in members if is_ability(f)}
      self._abilities.update(abilities)

      interactions = {name: f for name, f in members if is_interaction(f)}
      self._interactions.update(interactions)

  def call(self, interaction, **kwargs):
    # TODO: validation
    applicable_args = self._get_applicable_args(interaction, **kwargs)
    return interaction(**applicable_args)

  def attempts_to(self, task, **kwargs):
    return self.call(task, **kwargs)

  def asks_for(self, question, **kwargs):
    return self.call(question, **kwargs)

  def __getattr__(self, attr):
    # Try to get it as an ability
    if attr.startswith('can_'):
      ability_name = attr[4:]
      if ability_name not in self._abilities:
        raise UnknownAbilityError(ability_name)
      else:
        return functools.partial(self._can_do_ability, ability_name)

    # Fall back to get it as an interaction
    else:
      if attr not in self._interactions:
        raise UnknownInteractionError(attr)
      else:
        interaction = self._interactions[attr]
        return functools.partial(self.asks_for, interaction)


class UnknownAbilityError(Exception):
  def __init__(self, ability_name):
    super().__init__(f'The actor does not know "{ability_name}"')
    self.ability_name = ability_name


class UnknownInteractionError(Exception):
  def __init__(self, interaction_name):
    super().__init__(f'The actor does not know "{interaction_name}"')
    self.interaction_name = interaction_name
