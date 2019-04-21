import pytest

from screenplay import web
from screenplay.actor import Actor, UnknownInteractionError
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
  actor.can(browser=browser)
  return actor


def test_classic_actor_interactions(actor):
  response = actor.asks_for(web.existence, locator=GOOGLE_SEARCH_BOX)
  assert response


def test_pythonic_actor_interactions(actor):
  actor.knows(web)
  response = actor.existence(locator=GOOGLE_SEARCH_BOX)
  assert response


def test_unknown_actor_interaction(actor):
  actor.knows(web)
  with pytest.raises(UnknownInteractionError):
    actor.bark()
