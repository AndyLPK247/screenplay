import pytest

from screenplay import web
from screenplay.actor import init_actor, UnknowableArgumentError, UnknownSayingError
from selenium import webdriver
from selenium.webdriver.common.by import By


GOOGLE_SEARCH_BOX = web.Locator('Google Search Box', By.NAME, 'q')


@pytest.fixture
def browser():
  driver = webdriver.Firefox()
  driver.get("http://www.google.com")
  yield driver
  driver.quit()


@pytest.fixture
def actor(browser):
  actor = init_actor()
  actor.knows(web)
  actor.can_browse_the_web(browser=browser, timeout=30)
  return actor


def test_pythonic_actor_interactions(actor):
  response = actor.existence(locator=GOOGLE_SEARCH_BOX)
  assert response


def test_pythonic_actor_nonexistent_saying(actor):
  with pytest.raises(UnknownSayingError):
    actor.bark()


def test_pythonic_actor_know_invalid_arg(actor):
  with pytest.raises(UnknowableArgumentError):
    actor.knows(object())


# TODO: 'knows' tests for each screenplay function and traits
