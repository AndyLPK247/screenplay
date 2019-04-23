
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


# Exceptions

class NotScreenplayFunctionError(Exception):
  def __init__(self, func, functype):
    super().__init__(f'"{func.__name__}" is not {functype}')
    self.func = func


class NotAbilityError(Exception):
  def __init__(self, func):
    super().__init__(func, 'an ability')


class NotInteractionError(Exception):
  def __init__(self, func):
    super().__init__(func, 'an interaction')


class NotTaskError(Exception):
  def __init__(self, func):
    super().__init__(func, 'a task')


class NotQuestionError(Exception):
  def __init__(self, func):
    super().__init__(func, 'a question')


# Validations

def _validate_screenplay_func(func, predicate, exception):
    if not predicate(func):
      raise exception(func)


def validate_ability(ability):
  _validate_screenplay_func(ability, is_ability, NotAbilityError)


def validate_interaction(interaction):
  _validate_screenplay_func(interaction, is_interaction, NotInteractionError)


def validate_task(task):
  _validate_screenplay_func(task, is_task, NotTaskError)


def validate_question(question):
  _validate_screenplay_func(question, is_question, NotQuestionError)
