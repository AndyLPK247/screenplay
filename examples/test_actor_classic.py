import pytest

from screenplay.actor import Actor
from screenplay.web import Locator, existence
from selenium import webdriver
from selenium.webdriver.common.by import By


GOOGLE_SEARCH_BOX = Locator('Google Search Box', By.NAME, 'q')


@pytest.fixture
def browser():
  driver  = webdriver.Firefox()
  driver.get("http://www.google.com")
  yield driver
  driver.quit()


@pytest.fixture
def actor(browser):
  actor = Actor()
  actor.can(browser=browser, timeout=30)
  return actor


def test_classic_actor_interactions(actor):
  response = actor.asks_for(existence, locator=GOOGLE_SEARCH_BOX)
  assert response
