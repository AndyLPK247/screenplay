"""
This module contains Actor exceptions.
"""

# ------------------------------------------------------------------------------
# Actor Exceptions
# ------------------------------------------------------------------------------

class MissingParametersError(Exception):
  def __init__(self, interaction, parameters):
    super().__init__(f'{interaction.__name__} is missing the following parameters: {", ".join(parameters)}')
    self.interaction = interaction
    self.parameters = parameters


class UnknowableArgumentError(Exception):
  def __init__(self, argument):
    super().__init__(f'"{argument}" is not a module or screenplay function')
    self.argument = argument


class UnknownSayingError(Exception):
  def __init__(self, saying_name):
    super().__init__(f'The actor does not know "{saying_name}"')
    self.saying_name = saying_name
