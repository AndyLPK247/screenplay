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
  actor.knows(web)
  actor.can(**web.browse_the_web(browser, 30))
  return actor


def test_pythonic_actor_interactions(actor):
  response = actor.existence(locator=GOOGLE_SEARCH_BOX)
  assert response


def test_unknown_actor_interaction(actor):
  with pytest.raises(UnknownInteractionError):
    actor.bark()
