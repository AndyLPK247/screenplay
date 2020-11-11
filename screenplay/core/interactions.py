"""
This module contains decorators, functions, and exceptions for the Screenplay pattern.
These decorators enable regular functions to be used as Screenplay functions.
"""

# ------------------------------------------------------------------------------
# Interaction Decorators
# ------------------------------------------------------------------------------

def _screenplay_decorator(
  func,
  interaction=True,
  condition=False,
  question=False,
  task=False,
  extra_prefixes=None):

  func.is_interaction = interaction
  func.is_condition = condition
  func.is_question = question
  func.is_task = task
  func.phrases = [func.__name__, f'call_{func.__name__}']

  if extra_prefixes:
    for p in extra_prefixes:
      func.phrases.append(f'{p}{func.__name__}')

  return func


def interaction(func):
  return _screenplay_decorator(func)


def condition(func):
  return _screenplay_decorator(func, condition=True, extra_prefixes=['check_', 'asks_for_'])


def question(func):
  return _screenplay_decorator(func, question=True, extra_prefixes=['get_', 'asks_for_'])


def task(func):
  return _screenplay_decorator(func, task=True, extra_prefixes=['do_', 'attempts_to_'])


# ------------------------------------------------------------------------------
# Predicates
# ------------------------------------------------------------------------------

def _is_screenplay_func(func, attr):
  return callable(func) and hasattr(func, attr) and getattr(func, attr)


def is_interaction(func):
  return _is_screenplay_func(func, 'is_interaction')


def is_condition(func):
  return _is_screenplay_func(func, 'is_condition')


def is_question(func):
  return _is_screenplay_func(func, 'is_question')


def is_task(func):
  return _is_screenplay_func(func, 'is_task')


# ------------------------------------------------------------------------------
# Exceptions
# ------------------------------------------------------------------------------

class NotScreenplayFunctionError(Exception):
  def __init__(self, func, functype):
    super().__init__(f'"{func.__name__}" is not {functype}')
    self.func = func


class NotInteractionError(NotScreenplayFunctionError):
  def __init__(self, func):
    super().__init__(func, 'an interaction')


class NotConditionError(NotScreenplayFunctionError):
  def __init__(self, func):
    super().__init__(func, 'a condition')


class NotQuestionError(NotScreenplayFunctionError):
  def __init__(self, func):
    super().__init__(func, 'a question')


class NotTaskError(NotScreenplayFunctionError):
  def __init__(self, func):
    super().__init__(func, 'a task')


# ------------------------------------------------------------------------------
# Validations
# ------------------------------------------------------------------------------

def _validate_screenplay_func(func, predicate, exception):
    if not predicate(func):
      raise exception(func)


def validate_interaction(interaction):
  _validate_screenplay_func(interaction, is_interaction, NotInteractionError)


def validate_condition(condition):
  _validate_screenplay_func(condition, is_condition, NotConditionError)


def validate_question(question):
  _validate_screenplay_func(question, is_question, NotQuestionError)


def validate_task(task):
  _validate_screenplay_func(task, is_task, NotTaskError)
