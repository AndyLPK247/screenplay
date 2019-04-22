import pytest

from screenplay import web
from screenplay.actor import Actor, UnknownAbilityError, UnknownInteractionError
from selenium import webdriver
from selenium.webdriver.common.by import By


GOOGLE_SEARCH_BOX = web.Locator('Google Search Box', By.NAME, 'q')


@pytest.fixture
def browser():
  driver  = webdriver.Firefox()
  driver.get("http://www.google.com")
  yield driver
  driver.quit()


@pytest.fixture
def actor(browser):
  actor = Actor()
  actor.knows(web)
  actor.can_browse_the_web(browser, 30)
  return actor


def test_pythonic_actor_interactions(actor):
  response = actor.existence(locator=GOOGLE_SEARCH_BOX)
  assert response


def test_pythonic_actor_nonexistent_ability(actor):
  with pytest.raises(UnknownAbilityError):
    actor.can_bark()


def test_pythonic_actor_nonexistent_interaction(actor):
  with pytest.raises(UnknownInteractionError):
    actor.bark()


def test_pythonic_actor_noninteraction(actor):
  with pytest.raises(UnknownInteractionError):
    actor.noninteraction()
