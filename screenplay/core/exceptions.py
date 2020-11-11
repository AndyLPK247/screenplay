"""
This module contains Actor exceptions.
"""

# ------------------------------------------------------------------------------
# Actor Exceptions
# ------------------------------------------------------------------------------

class DuplicatePhraseError(Exception):
  def __init__(self, phrase, interaction):
    super().__init__(f'The actor already has the phrase "{phrase}"')
    self.phrase = phrase
    self.interaction = interaction


class MissingParametersError(Exception):
  def __init__(self, interaction, parameters):
    super().__init__(f'{interaction.__name__} is missing the following parameters: {", ".join(parameters)}')
    self.interaction = interaction
    self.parameters = parameters


class UnknowableArgumentError(Exception):
  def __init__(self, argument):
    super().__init__(f'"{argument}" is not a module or screenplay function')
    self.argument = argument


class UnknownPhraseError(Exception):
  def __init__(self, phrase):
    super().__init__(f'The actor does not know "{phrase}"')
    self.phrase = phrase
