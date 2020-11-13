"""
Contains interactions for Selenium WebDriver.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

from abc import ABC
from screenplay.conditions import IsTrue
from screenplay.core import Question, Task
from screenplay.waiting import WaitUntil
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException


# --------------------------------------------------------------------------------
# Class: Locator
# --------------------------------------------------------------------------------

class Locator:

  def __init__(self, name, qtype, query):
    self.name = name
    self.qtype = qtype
    self.query = query

  def __str__(self):
    return self.name

  def __repr__(self):
    return f"{self.qtype}: {self.query}"


# --------------------------------------------------------------------------------
# Abstract Class: LocatorInteraction
# --------------------------------------------------------------------------------

class LocatorInteraction(ABC):

  def __init__(self, locator):
    self.locator = locator
  
  def loc(self):
    return (self.locator.qtype, self.locator.query)


# --------------------------------------------------------------------------------
# Question: AppearanceOf
# --------------------------------------------------------------------------------

class AppearanceOf(Question, LocatorInteraction):

  def request_as(self, actor):
    try:
      driver = actor.using('webdriver')
      appeared = driver.find_element(*self.loc()).is_displayed()
    except (NoSuchElementException, StaleElementReferenceException):
      # if the element isn't found, then it doesn't exist
      appeared = False
    return appeared

  def __str__(self):
    return f'appearance of {self.locator}'


# --------------------------------------------------------------------------------
# Task: Clear
# --------------------------------------------------------------------------------

class Clear(Task, LocatorInteraction):

  def perform_as(self, actor):
    actor.attempts_to(WaitUntil(AppearanceOf(self.locator), IsTrue()))
    driver = actor.using('webdriver')
    driver.find_element(*self.loc()).clear()
    
  def __str__(self):
    return f'clear {self.locator}'


# --------------------------------------------------------------------------------
# Question: ExistenceOf
# --------------------------------------------------------------------------------

class ExistenceOf(Question, LocatorInteraction):

  def request_as(self, actor):
    driver = actor.using('webdriver')
    elements = driver.find_elements(*self.loc())
    return len(elements) > 0

  def __str__(self):
    return f'existence of {self.locator}'


# --------------------------------------------------------------------------------
# Task: NavigateToUrl
# --------------------------------------------------------------------------------

class NavigateToUrl(Task):

  def __init__(self, url):
    self.url = url

  def perform_as(self, actor):
    actor.using('webdriver').get(self.url)
    
  def __str__(self):
    return f'navigate to {self.url}'


# --------------------------------------------------------------------------------
# Task: QuitBrowser
# --------------------------------------------------------------------------------

class QuitBrowser(Task):

  def perform_as(self, actor):
    actor.using('webdriver').quit()
    
  def __str__(self):
    return f'quit the browser'