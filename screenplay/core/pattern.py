"""
This module contains decorators, functions, and exceptions for the Screenplay pattern.
These decorators enable regular functions to be used as Screenplay functions.
"""

# ------------------------------------------------------------------------------
# Decorators
# ------------------------------------------------------------------------------

def _screenplay_decorator(
  func,
  condition=False,
  interaction=False,
  task=False,
  question=False,
  saying=False):

  func.is_condition = condition
  func.is_interaction = interaction
  func.is_task = task
  func.is_question = question
  func.is_saying = saying
  return func


def condition(func):
  return _screenplay_decorator(func, condition=True)


def interaction(func):
  return _screenplay_decorator(func, interaction=True)


def task(func):
  return _screenplay_decorator(func, interaction=True, task=True)


def question(func):
  return _screenplay_decorator(func, interaction=True, question=True)


def saying(func):
  return _screenplay_decorator(func, saying=True)


# ------------------------------------------------------------------------------
# Predicates
# ------------------------------------------------------------------------------

def _is_screenplay_func(func, attr):
  return callable(func) and hasattr(func, attr) and getattr(func, attr)


def is_condition(func):
  return _is_screenplay_func(func, 'is_condition')


def is_interaction(func):
  return _is_screenplay_func(func, 'is_interaction')


def is_task(func):
  return _is_screenplay_func(func, 'is_task')


def is_question(func):
  return _is_screenplay_func(func, 'is_question')


def is_saying(func):
  return _is_screenplay_func(func, 'is_saying')


# ------------------------------------------------------------------------------
# Exceptions
# ------------------------------------------------------------------------------

class NotScreenplayFunctionError(Exception):
  def __init__(self, func, functype):
    super().__init__(f'"{func.__name__}" is not {functype}')
    self.func = func


class NotConditionError(NotScreenplayFunctionError):
  def __init__(self, func):
    super().__init__(func, 'a condition')


class NotInteractionError(NotScreenplayFunctionError):
  def __init__(self, func):
    super().__init__(func, 'an interaction')


class NotTaskError(NotScreenplayFunctionError):
  def __init__(self, func):
    super().__init__(func, 'a task')


class NotQuestionError(NotScreenplayFunctionError):
  def __init__(self, func):
    super().__init__(func, 'a question')


class NotSayingError(NotScreenplayFunctionError):
  def __init__(self, func):
    super().__init__(func, 'a saying')


# ------------------------------------------------------------------------------
# Validations
# ------------------------------------------------------------------------------

def _validate_screenplay_func(func, predicate, exception):
    if not predicate(func):
      raise exception(func)


def validate_condition(condition):
  _validate_screenplay_func(condition, is_condition, NotConditionError)


def validate_interaction(interaction):
  _validate_screenplay_func(interaction, is_interaction, NotInteractionError)


def validate_task(task):
  _validate_screenplay_func(task, is_task, NotTaskError)


def validate_question(question):
  _validate_screenplay_func(question, is_question, NotQuestionError)


def validate_saying(saying):
  _validate_screenplay_func(saying, is_saying, NotSayingError)
