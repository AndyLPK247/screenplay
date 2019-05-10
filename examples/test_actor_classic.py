import pytest

from screenplay.actor import screenplay_actor
from screenplay.web import Locator, browse_the_web, existence
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
  actor = screenplay_actor()
  actor.can(browse_the_web, browser=browser, timeout=30)
  return actor


def test_classic_actor_interactions(actor):
  response = actor.asks_for(existence, locator=GOOGLE_SEARCH_BOX)
  assert response


# Test Actor

# initial actor is empty
# know traits
# know abilities
# know interactions
# know sayings
# know actor
# know module
# know multiple
# know duplicate
# know none of the above
# can ability without args
# can ability with args
# can unknown ability
# can non-ability
# can duplicate traits
# call interaction without parameters
# call interaction without args and no traits
# call interaction with args and no traits
# call interaction without args and with traits
# call interaction with some args and traits
# call interaction with unnecessary traits
# call interaction with unnecessary args
# call interaction with missing parameters
# call interaction with actor parameter
# can unknown interaction
# call non-interaction
# getattr no sayings
# getattr match saying
# getattr unmatched saying
# getattr match first of multiple sayings


# Test Sayings

# call_ability: "can_" success
# call_ability: "can_" DNE
# call_interaction: success without parameters
# call_interaction: success with args only
# call_interaction: success with args and traits
# call_interaction: success with extra args
# call_interaction: DNE
# attempts_to: task
# attempts_to: interaction
# attempts_to: raw function
# asks_for: question
# asks_for: interaction
# asks_for: raw function


# Test Wait Interactions

# wait: defaults
# wait: arg values
# on: question without args
# on: question with args
# on: non-question
# to: condition without args
# to: condition with args
# to: non-condition
# to: success with no need to wait
# to: success after waiting
# to: no success after waiting (explicit timeout and interval)
# chain: actor.attempts_to(wait, timeout=30, interval=1).on(question, **).to(condition, **)
# chain: actor.attempts_to(wait, timeout=30, interval=1).on(question).to(condition)
# chain: actor.wait(timeout=30, interval=1).on(question).to(question)
# chain: actor.wait().on(question).to(question)


# Future Tests

# actor.wait().on_something(locator=SOME_ELEMENT).to_be(value=789)
# actor.wait_on_something(locator=SOME_ELEMENT).to_be(value=789)
# actor.wait_on_something(locator=SOME_ELEMENT).to_be(789)
# actor.wait_on_something(locator=SOME_ELEMENT).to_match("regex")
# actor.wait_on_something(locator=SOME_ELEMENT).to_contain_substring("substring")
# actor.wait_on_something(locator=SOME_ELEMENT).to_contain("a", "b", "c")
