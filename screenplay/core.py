"""
Contains the core definitions for the Screenplay Pattern.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

import logging

from abc import ABC, abstractmethod


# --------------------------------------------------------------------------------
# Logging
# --------------------------------------------------------------------------------

logger = logging.getLogger(__name__)


# --------------------------------------------------------------------------------
# Class: Actor
# --------------------------------------------------------------------------------

class Actor:

  def __init__(self, name='Actor'):
    self.name = name
    self._abilities = dict()

  def can_use(self, **kwargs):
    self._abilities.update(kwargs)
    logger.debug(f'{self} can use: {kwargs}')

  def has(self, ability):
    return ability in self._abilities

  def using(self, ability):
    if not self.has(ability):
      raise MissingAbilityException(self, ability)
    value = self._abilities[ability]
    logger.debug(f'{self} is using "{ability}" as "{value}"')
    return value

  def attempts_to(self, task):
    logger.info(f'{self} attempts to {task}')
    answer = task.perform_as(self)
    logger.info(f'{self} did {task}')
    return answer

  def asks_for(self, question):
    logger.info(f'{self} asks for {question}')
    answer = question.request_as(self)
    logger.info(f'{self} asked for {question} and got {answer}')
    return answer

  def calls(self, interaction):
    logger.info(f'{self} calls {interaction}')
    if isinstance(interaction, Task):
      answer = interaction.perform_as(self)
    elif isinstance(interaction, Question):
      answer = interaction.request_as(self)
    if answer is None:
      logger.info(f'{self} called {interaction}')
    else:
      logger.info(f'{self} called {interaction} and got {answer}')
    return answer

  def __str__(self):
    return self.name


# --------------------------------------------------------------------------------
# Abstract Class: Interaction
# --------------------------------------------------------------------------------

class Interaction(ABC):
  pass


# --------------------------------------------------------------------------------
# Abstract Class: Task
# --------------------------------------------------------------------------------

class Task(Interaction, ABC):
  @abstractmethod
  def perform_as(self, actor):
    pass


# --------------------------------------------------------------------------------
# Abstract Class: Question
# --------------------------------------------------------------------------------

class Question(Interaction, ABC):
  @abstractmethod
  def request_as(self, actor):
    pass


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
