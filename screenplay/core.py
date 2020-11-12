"""
Contains the core definitions for the Screenplay Pattern.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

from abc import ABC, abstractmethod


# --------------------------------------------------------------------------------
# Class: ScreenplayException
# --------------------------------------------------------------------------------

class ScreenplayException(Exception):
  def __init__(self, message):
    super().__init__(message)


# --------------------------------------------------------------------------------
# Class: MissingAbilityException
# --------------------------------------------------------------------------------

class MissingAbilityException(ScreenplayException):
  def __init__(self, actor, ability):
    super().__init__(f'The actor "{actor}" does not have an ability named "{ability}"')
    self.actor = actor
    self.ability = ability


# --------------------------------------------------------------------------------
# Class: Actor
# --------------------------------------------------------------------------------

class Actor:

  def __init__(self, name='Actor'):
    self._abilities = dict()
    self._name = name

  def can_use(self, **kwargs):
    self._abilities.update(kwargs)

  def has(self, ability):
    return ability in self._abilities

  def using(self, ability):
    if not self.has(ability):
      raise MissingAbilityException(self, ability)
    return self._abilities[ability]

  def attempts_to(self, task):
    task.perform_as(self)

  def asks_for(self, question):
    return question.request_as(self)

  def __str__(self):
    return self._name


# --------------------------------------------------------------------------------
# Class: Interaction
# --------------------------------------------------------------------------------

class Interaction:
  pass


# --------------------------------------------------------------------------------
# Class: Task
# --------------------------------------------------------------------------------

class Task(Interaction, ABC):
  
  @abstractmethod
  def perform_as(self, actor):
    pass


# --------------------------------------------------------------------------------
# Class: Question
# --------------------------------------------------------------------------------

class Question(Interaction, ABC):
  
  @abstractmethod
  def request_as(self, actor):
    pass
