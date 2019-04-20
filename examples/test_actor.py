import pytest
import screenplay.interactions as interactions

from screenplay.actor import Actor, UnknownInteractionError


def test_classic_actor_interactions():
  actor = Actor()
  actor.can(webdriver='chrome')
  response = actor.attempts_to(interactions.click, locator='button')
  assert response


def test_pythonic_actor_interactions():
  actor = Actor()
  actor.can(webdriver='chrome')
  actor.knows(interactions)
  response = actor.click(locator='button')
  assert response


def test_unknown_actor_interaction():
  actor = Actor()
  actor.can(webdriver='chrome')
  actor.knows(interactions)
  with pytest.raises(UnknownInteractionError):
    actor.bark()
  