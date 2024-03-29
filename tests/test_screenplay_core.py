"""
Contains unit tests for the screenplay.core module.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

import pytest

from screenplay.core import Actor, Task, Question, MissingAbilityException


# --------------------------------------------------------------------------------
# Fixtures
# --------------------------------------------------------------------------------

@pytest.fixture
def actor():
  return Actor()


# --------------------------------------------------------------------------------
# Tests: Actor
# --------------------------------------------------------------------------------

def test_actor_init_default(actor):
  assert len(actor._abilities) == 0
  assert str(actor) == 'Actor'


def test_actor_init_with_name():
  andy = Actor('Andy')
  assert andy.name == 'Andy'
  assert str(andy) == 'Andy'
  assert len(andy._abilities) == 0


def test_actor_has_an_ability(actor):
  actor.can_use(thing='tool')
  assert actor.has('thing')


def test_actor_does_not_have_an_ability(actor):
  actor.can_use(thing='tool')
  assert not actor.has('other')


def test_actor_has_multiple_abilities(actor):
  actor.can_use(thing='tool1', other='tool2')
  actor.can_use(third='tool3')
  assert actor.has('thing')
  assert actor.has('other')
  assert actor.has('third')
  assert not actor.has('tool1')
  assert not actor.has('tool2')
  assert not actor.has('tool3')


def test_actor_using_an_ability(actor):
  actor.can_use(thing='tool')
  assert actor.using('thing') == 'tool'


def test_actor_using_one_of_multiple_ability(actor):
  actor.can_use(thing='tool1', other='tool2')
  actor.can_use(third='tool3')
  assert actor.using('other') == 'tool2'


def test_actor_using_a_missing_ability_raises_an_exception(actor):
  with pytest.raises(MissingAbilityException) as e:
    actor.using('thing')
  assert e.value.actor == actor
  assert e.value.ability == 'thing'
  assert str(e.value) == 'The actor "Actor" does not have an ability named "thing"'


# --------------------------------------------------------------------------------
# Tests: Task
# --------------------------------------------------------------------------------

class AddAnAbility(Task):

  def __init__(self, name):
    self.name = name

  def perform_as(self, actor):
    actor.can_use(new_ability=self.name)


class UseAnAbility(Task):

  def perform_as(self, actor):
    value = actor.using('thing')
    actor.can_use(new_ability=value)


def test_actor_attempts_a_task_with_an_argument(actor):
  actor.attempts_to(AddAnAbility('cool'))
  assert actor.has('new_ability')
  assert actor.using('new_ability') == 'cool'


def test_actor_attempts_a_task_that_uses_an_ability(actor):
  actor.can_use(thing='cool')
  actor.attempts_to(UseAnAbility())
  assert actor.has('new_ability')
  assert actor.using('new_ability') == 'cool'


def test_actor_attempts_a_task_but_lacks_the_ability(actor):
  with pytest.raises(MissingAbilityException):
    actor.attempts_to(UseAnAbility())


def test_actor_calls_a_task_with_an_argument(actor):
  actor.calls(AddAnAbility('cool'))
  assert actor.has('new_ability')
  assert actor.using('new_ability') == 'cool'


def test_actor_calls_a_task_that_uses_an_ability(actor):
  actor.can_use(thing='cool')
  actor.calls(UseAnAbility())
  assert actor.has('new_ability')
  assert actor.using('new_ability') == 'cool'


def test_actor_calls_a_task_but_lacks_the_ability(actor):
  with pytest.raises(MissingAbilityException):
    actor.calls(UseAnAbility())


# --------------------------------------------------------------------------------
# Tests: Question
# --------------------------------------------------------------------------------

class AddingOne(Question):

  def __init__(self, amount):
    self.amount = amount

  def request_as(self, actor):
    return self.amount + 1


class AddingOneToStart(Question):

  def request_as(self, actor):
    return actor.using('start') + 1


def test_actor_asks_for_a_question_with_an_argument(actor):
  answer = actor.asks_for(AddingOne(5))
  assert answer == 6


def test_actor_asks_for_a_question_that_uses_an_ability(actor):
  actor.can_use(start=9)
  answer = actor.asks_for(AddingOneToStart())
  assert answer == 10


def test_actor_asks_for_a_question_but_lacks_the_ability(actor):
  with pytest.raises(MissingAbilityException):
    actor.asks_for(AddingOneToStart())


def test_actor_calls_a_question_with_an_argument(actor):
  answer = actor.calls(AddingOne(5))
  assert answer == 6


def test_actor_calls_a_question_that_uses_an_ability(actor):
  actor.can_use(start=9)
  answer = actor.calls(AddingOneToStart())
  assert answer == 10


def test_actor_calls_a_question_but_lacks_the_ability(actor):
  with pytest.raises(MissingAbilityException):
    actor.calls(AddingOneToStart())
