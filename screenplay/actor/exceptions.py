"""
This module contains Actor exceptions.
"""

# ------------------------------------------------------------------------------
# Actor Exceptions
# ------------------------------------------------------------------------------

class MissingParameterError(Exception):
  def __init__(self, parameter, interaction):
    super().__init__(f'Parameter "{parameter}" is missing for {interaction.__name__}')
    self.parameter = parameter
    self.interaction = interaction


class UnknowableArgumentError(Exception):
  def __init__(self, argument):
    super().__init__(f'"{argument}" is not a module or screenplay function')
    self.argument = argument


class UnknownSayingError(Exception):
  def __init__(self, saying_name):
    super().__init__(f'The actor does not know "{saying_name}"')
    self.saying_name = saying_name
