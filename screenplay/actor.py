import functools
import inspect


class Actor:
  def __init__(self):
    self._abilities = dict()
    self._callables = dict()
  
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
      elif name in self._abilities:
        applicable_args[name] = self._abilities[name]
      elif param.default == inspect.Parameter.empty:
        raise Exception(f"Parameter '{name}' is missing for {func.__name__}")
    
    return applicable_args

  def can(self, **kwargs):
    self._abilities.update(kwargs)

  def knows(self, *args):
    for module in args:
      members = inspect.getmembers(module)
      functions = {name: c for name, c in members if callable(c)}
      self._callables.update(functions)

  def call(self, interaction, **kwargs):
    applicable_args = self._get_applicable_args(interaction, **kwargs)
    return interaction(**applicable_args)

  def attempts_to(self, task, **kwargs):
    return self.call(task, **kwargs)

  def asks_for(self, question, **kwargs):
    return self.call(question, **kwargs)

  def __getattr__(self, attr):
    if attr not in self._callables:
      raise UnknownInteractionError(f'The actor does not know "{attr}"')
      
    known_func = self._callables[attr]
    return functools.partial(self.asks_for, known_func)


class UnknownInteractionError(Exception):
  def __init__(self, interaction_name):
    super().__init__(f'The actor does not know "{interaction_name}"')
    self.interaction_name = interaction_name
