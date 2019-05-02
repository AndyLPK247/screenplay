from screenplay.pattern import ability, question


# Locator

class Locator:
  def __init__(self, name, by, query):
    self.name = name
    self.by = by
    self.query = query

  def __str__(self):
    return f'{self.name} ({self.by}: {self.query})'


# Abilities

@ability
def browse_the_web(browser, timeout):
  return {'browser': browser, 'timeout': timeout}


# Tasks


# Questions

@question
def appearance(locator, browser):
  return existence(locator, browser) and \
    browser.find_element(locator.by).is_displayed()


@question
def existence(locator, browser):
  elements = browser.find_elements(locator.by, locator.query)
  return len(elements) > 0


# Temporary
def noninteraction():
  pass
