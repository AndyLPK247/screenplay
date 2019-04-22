
# Decorators

def ability(func):
  func.is_ability = True
  return func


def interaction(func):
  func.is_interaction = True
  func.is_task = False
  func.is_question = False
  return func


def task(func):
  func.is_interaction = True
  func.is_task = True
  func.is_question = False
  return func


def question(func):
  func.is_interaction = True
  func.is_task = False
  func.is_question = True
  return func


# Predicates

def _is_screenplay_func(func, attr):
  return callable(func) and hasattr(func, attr) and getattr(func, attr)


def is_ability(func):
  return _is_screenplay_func(func, 'is_ability')


def is_interaction(func):
  return _is_screenplay_func(func, 'is_interaction')


def is_task(func):
  return _is_screenplay_func(func, 'is_task')


def is_question(func):
  return _is_screenplay_func(func, 'is_question')
