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
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


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
# Task: Click
# --------------------------------------------------------------------------------

class Click(Task, LocatorInteraction):

  def perform_as(self, actor):
    actor.attempts_to(WaitUntil(AppearanceOf(self.locator), IsTrue()))
    driver = actor.using('webdriver')
    element = driver.find_element(*self.loc())
    ActionChains(driver).move_to_element(element).click().perform()
    
  def __str__(self):
    return f'click {self.locator}'


# --------------------------------------------------------------------------------
# Question: CountOf
# --------------------------------------------------------------------------------

class CountOf(Question, LocatorInteraction):

  def request_as(self, actor):
    driver = actor.using('webdriver')
    elements = driver.find_elements(*self.loc())
    return len(elements)

  def __str__(self):
    return f'count of {self.locator}'


# --------------------------------------------------------------------------------
# Question: CurrentUrl
# --------------------------------------------------------------------------------

class CurrentUrl(Question):

  def request_as(self, actor):
    return actor.using('webdriver').current_url

  def __str__(self):
    return f'current URL'


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
# Task: HoverOver
# --------------------------------------------------------------------------------

class HoverOver(Task, LocatorInteraction):

  def perform_as(self, actor):
    actor.attempts_to(WaitUntil(AppearanceOf(self.locator), IsTrue()))
    driver = actor.using('webdriver')
    element = driver.find_element(*self.loc())
    ActionChains(driver).move_to_element(element).perform()
    
  def __str__(self):
    return f'hover over {self.locator}'


# --------------------------------------------------------------------------------
# Task: MaximizeWindow
# --------------------------------------------------------------------------------

class MaximizeWindow(Task):

  def perform_as(self, actor):
    actor.using('webdriver').maximize_window()
    
  def __str__(self):
    return f'maximize the browser window'


# --------------------------------------------------------------------------------
# Task: MinimizeWindow
# --------------------------------------------------------------------------------

class MinimizeWindow(Task):

  def perform_as(self, actor):
    actor.using('webdriver').minimize_window()
    
  def __str__(self):
    return f'minimize the browser window'


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


# --------------------------------------------------------------------------------
# Task: RefreshBrowser
# --------------------------------------------------------------------------------

class RefreshBrowser(Task):

  def perform_as(self, actor):
    actor.using('webdriver').refresh()
    
  def __str__(self):
    return f'refresh the browser'


# --------------------------------------------------------------------------------
# Task: SendKeysTo
# --------------------------------------------------------------------------------

class SendKeysTo(Task, LocatorInteraction):

  def __init__(self, locator, keys, clear=True, enter=False):
    super().__init__(locator)
    self.keys = keys
    self.clear = clear
    self.enter = enter

  def _get_keys(self):
    return self.keys + Keys.ENTER if self.enter else self.keys

  def perform_as(self, actor):
    actor.attempts_to(WaitUntil(AppearanceOf(self.locator), IsTrue()))
    driver = actor.using('webdriver')
    element = driver.find_element(*self.loc())
    if self.clear:
      element.clear()
    element.send_keys(self._get_keys())
    
  def __str__(self):
    return f'send keys "{self.keys}" to {self.locator}'


# --------------------------------------------------------------------------------
# Task: Submit
# --------------------------------------------------------------------------------

class Submit(Task, LocatorInteraction):

  def perform_as(self, actor):
    actor.attempts_to(WaitUntil(ExistenceOf(self.locator), IsTrue()))
    driver = actor.using('webdriver')
    driver.find_element(*self.loc()).submit()
    
  def __str__(self):
    return f'submit {self.locator}'


# --------------------------------------------------------------------------------
# Question: Title
# --------------------------------------------------------------------------------

class Title(Question):

  def request_as(self, actor):
    return actor.using('webdriver').title

  def __str__(self):
    return f'title'


# --------------------------------------------------------------------------------
# Question: TextListOf
# --------------------------------------------------------------------------------

class TextListOf(Question, LocatorInteraction):

  def request_as(self, actor):
    actor.attempts_to(WaitUntil(ExistenceOf(self.locator), IsTrue()))
    driver = actor.using('webdriver')
    elements = driver.find_elements(*self.loc())
    return [x.text for x in elements]

  def __str__(self):
    return f'text of {self.locator}'


# --------------------------------------------------------------------------------
# Question: TextOf
# --------------------------------------------------------------------------------

class TextOf(Question, LocatorInteraction):

  def request_as(self, actor):
    actor.attempts_to(WaitUntil(ExistenceOf(self.locator), IsTrue()))
    driver = actor.using('webdriver')
    return driver.find_element(*self.loc()).text

  def __str__(self):
    return f'text of {self.locator}'


# --------------------------------------------------------------------------------
# Question: WindowHandles
# --------------------------------------------------------------------------------

class WindowHandles(Question):

  def request_as(self, actor):
    return actor.using('webdriver').window_handles

  def __str__(self):
    return f'window handles'
