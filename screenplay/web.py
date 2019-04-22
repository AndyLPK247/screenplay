from screenplay.decorators import ability, interaction


class Locator:
  def __init__(self, name, by, query):
    self.name = name
    self.by = by
    self.query = query

  def __str__(self):
    return f'{self.name} ({self.by}: {self.query})'


@ability
def browse_the_web(browser, timeout):
  return {'browser': browser, 'timeout': timeout}


@interaction
def existence(locator, browser):
  elements = browser.find_elements(locator.by, locator.query)
  return len(elements) > 0


# Temporary
def noninteraction():
  pass
