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
from selenium.webdriver.support.ui import Select


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
# Abstract Class: SelectInteraction
# --------------------------------------------------------------------------------

class SelectInteraction(LocatorInteraction, ABC):

  def get_select(self, actor):
    actor.attempts_to(WaitUntil(ExistenceOf(self.locator), IsTrue()))
    driver = actor.using('webdriver')
    select = Select(driver.find_element(*self.loc()))
    return select


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
# Question: CssClassesOf
# --------------------------------------------------------------------------------

class CssClassesOf(Question, LocatorInteraction):

  def __init__(self, locator):
    super().__init__(locator)

  def request_as(self, actor):
    actor.attempts_to(WaitUntil(ExistenceOf(self.locator), IsTrue()))
    driver = actor.using('webdriver')
    classes = driver.find_element(*self.loc()).get_attribute('class')
    return classes.split()

  def __str__(self):
    return f'CSS classes of {self.locator}'


# --------------------------------------------------------------------------------
# Question: CssPropertyValueOf
# --------------------------------------------------------------------------------

class CssPropertyValueOf(Question, LocatorInteraction):

  def __init__(self, locator, prop_name):
    super().__init__(locator)
    self.prop_name = prop_name

  def request_as(self, actor):
    actor.attempts_to(WaitUntil(ExistenceOf(self.locator), IsTrue()))
    driver = actor.using('webdriver')
    return driver.find_element(*self.loc()).value_of_css_property(self.prop_name)

  def __str__(self):
    return f'CSS property value "{self.prop_name}" of {self.locator}'


# --------------------------------------------------------------------------------
# Question: CurrentUrl
# --------------------------------------------------------------------------------

class CurrentUrl(Question):

  def request_as(self, actor):
    return actor.using('webdriver').current_url

  def __str__(self):
    return f'current URL'


# --------------------------------------------------------------------------------
# Question: EnabledStateOf
# --------------------------------------------------------------------------------

class EnabledStateOf(Question, LocatorInteraction):

  def request_as(self, actor):
    actor.attempts_to(WaitUntil(ExistenceOf(self.locator), IsTrue()))
    driver = actor.using('webdriver')
    return driver.find_element(*self.loc()).is_enabled()

  def __str__(self):
    return f'enabled state of {self.locator}'


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
# Question: HtmlAttributeOf
# --------------------------------------------------------------------------------

class HtmlAttributeOf(Question, LocatorInteraction):

  def __init__(self, locator, attribute):
    super().__init__(locator)
    self.attribute = attribute

  def request_as(self, actor):
    actor.attempts_to(WaitUntil(ExistenceOf(self.locator), IsTrue()))
    driver = actor.using('webdriver')
    return driver.find_element(*self.loc()).get_attribute(self.attribute)

  def __str__(self):
    return f'HTML attribute "{self.attribute}" of {self.locator}'


# --------------------------------------------------------------------------------
# Question: JavaScriptInBrowser
# --------------------------------------------------------------------------------

class JavaScriptInBrowser(Question):

  def __init__(self, script, *args):
    self.script = script
    self.args = args

  def request_as(self, actor):
    driver = actor.using('webdriver')
    return driver.execute_script(self.script, *self.args)

  def __str__(self):
    return f'JavaScript "{self.script}" with {self.args}'


# --------------------------------------------------------------------------------
# Question: LocationOf
# --------------------------------------------------------------------------------

class LocationOf(Question, LocatorInteraction):

  def request_as(self, actor):
    actor.attempts_to(WaitUntil(ExistenceOf(self.locator), IsTrue()))
    driver = actor.using('webdriver')
    return driver.find_element(*self.loc()).location

  def __str__(self):
    return f'location of {self.locator}'


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
# Question: PixelSizeOf
# --------------------------------------------------------------------------------

class PixelSizeOf(Question, LocatorInteraction):

  def request_as(self, actor):
    actor.attempts_to(WaitUntil(ExistenceOf(self.locator), IsTrue()))
    driver = actor.using('webdriver')
    return driver.find_element(*self.loc()).size

  def __str__(self):
    return f'pixel size of {self.locator}'


# --------------------------------------------------------------------------------
# Question: PropertyOf
# --------------------------------------------------------------------------------

class PropertyOf(Question, LocatorInteraction):

  def __init__(self, locator, prop_name):
    super().__init__(locator)
    self.prop_name = prop_name

  def request_as(self, actor):
    actor.attempts_to(WaitUntil(ExistenceOf(self.locator), IsTrue()))
    driver = actor.using('webdriver')
    return driver.find_element(*self.loc()).get_property(self.prop_name)

  def __str__(self):
    return f'Property "{self.prop_name}" of {self.locator}'


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
# Task: SaveScreenshotTo
# --------------------------------------------------------------------------------

class SaveScreenshotTo(Task):

  def __init__(self, png_path):
    self.png_path = png_path

  def perform_as(self, actor):
    actor.using('webdriver').save_screenshot(self.png_path)

  def __str__(self):
    return f'save screenshot to {self.png_path}'


# --------------------------------------------------------------------------------
# Question: ScreenshotAsBase64
# --------------------------------------------------------------------------------

class ScreenshotAsBase64(Question):

  def request_as(self, actor):
    return actor.using('webdriver').get_screenshot_as_base64()

  def __str__(self):
    return f'screenshot as a base64 encoded string'


# --------------------------------------------------------------------------------
# Question: ScreenshotAsPng
# --------------------------------------------------------------------------------

class ScreenshotAsPng(Question):

  def request_as(self, actor):
    return actor.using('webdriver').get_screenshot_as_png()

  def __str__(self):
    return f'screenshot as PNG binary data'


# --------------------------------------------------------------------------------
# Task: SelectByIndex
# --------------------------------------------------------------------------------

class SelectByIndex(Task, SelectInteraction):

  def __init__(self, locator, index):
    super().__init__(locator)
    self.index = index

  def perform_as(self, actor):
    select = self.get_select(actor)
    select.select_by_index(self.index)
    
  def __str__(self):
    return f'select {self.locator} by index "{self.index}"'


# --------------------------------------------------------------------------------
# Task: SelectByText
# --------------------------------------------------------------------------------

class SelectByText(Task, SelectInteraction):

  def __init__(self, locator, text):
    super().__init__(locator)
    self.text = text

  def perform_as(self, actor):
    select = self.get_select(actor)
    select.select_by_visible_text(self.text)
    
  def __str__(self):
    return f'select {self.locator} by text "{self.text}"'


# --------------------------------------------------------------------------------
# Task: SelectByValue
# --------------------------------------------------------------------------------

class SelectByValue(Task, SelectInteraction):

  def __init__(self, locator, value):
    super().__init__(locator)
    self.value = value

  def perform_as(self, actor):
    select = self.get_select(actor)
    select.select_by_value(self.value)
    
  def __str__(self):
    return f'select {self.locator} by value "{self.value}"'


# --------------------------------------------------------------------------------
# Task: SelectOptionsTextList
# --------------------------------------------------------------------------------

class SelectOptionsTextList(Question, SelectInteraction):

  def request_as(self, actor):
    return [o.text for o in self.get_select(actor).options]
    
  def __str__(self):
    return 'select options'


# --------------------------------------------------------------------------------
# Task: SelectedOptionsTextList
# --------------------------------------------------------------------------------

class SelectedOptionsTextList(Question, SelectInteraction):

  def request_as(self, actor):
    return [o.text for o in self.get_select(actor).all_selected_options]
    
  def __str__(self):
    return 'selected options'


# --------------------------------------------------------------------------------
# Question: SelectedStateOf
# --------------------------------------------------------------------------------

class SelectedStateOf(Question, LocatorInteraction):

  def request_as(self, actor):
    actor.attempts_to(WaitUntil(ExistenceOf(self.locator), IsTrue()))
    driver = actor.using('webdriver')
    return driver.find_element(*self.loc()).is_selected()

  def __str__(self):
    return f'selected state of {self.locator}'


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
# Question: TagNameOf
# --------------------------------------------------------------------------------

class TagNameOf(Question, LocatorInteraction):

  def request_as(self, actor):
    actor.attempts_to(WaitUntil(ExistenceOf(self.locator), IsTrue()))
    driver = actor.using('webdriver')
    return driver.find_element(*self.loc()).tag_name

  def __str__(self):
    return f'tag name of {self.locator}'


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
# Question: ValueAttributeOf
# --------------------------------------------------------------------------------

class ValueAttributeOf(HtmlAttributeOf):
  def __init__(self, locator):
    super().__init__(locator, 'value')


# --------------------------------------------------------------------------------
# Question: WindowHandles
# --------------------------------------------------------------------------------

class WindowHandles(Question):

  def request_as(self, actor):
    return actor.using('webdriver').window_handles

  def __str__(self):
    return f'window handles'
