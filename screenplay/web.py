"""
This module provides interactions for Web UI browser automation.
It uses Selenium WebDriver.
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

from screenplay.core.pattern import question, task
from screenplay.core.wait import wait


# ------------------------------------------------------------------------------
# Locator Class
# ------------------------------------------------------------------------------

class Locator:
  def __init__(self, name, by, query):
    self.name = name
    self.by = by
    self.query = query

  def __str__(self):
    return f'{self.name} ({self.by}: {self.query})'


# ------------------------------------------------------------------------------
# Tasks
# ------------------------------------------------------------------------------

# @task
# def click(actor, locator, browser):
#   actor.wait().on(question=appearance, locator=locator).to(condition=be, value=true)
#   # TODO: should web actors know all web interactions, waiting, and conditions?


# ------------------------------------------------------------------------------
# Questions
# ------------------------------------------------------------------------------

@question
def appearance(browser, locator):
  return existence(locator, browser) and \
    browser.find_element(locator.by).is_displayed()


@question
def existence(browser, locator):
  elements = browser.find_elements(locator.by, locator.query)
  return len(elements) > 0
