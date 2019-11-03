"""
This module contains builders for the Actor class.
The 'init_actor' constructs the standard Pythonic Screenplay Actor.
As a best practice, only use builders to initialize Actor instances.
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

from screenplay.core.actor import Actor
from screenplay.core.sayings import ask_question, call_interaction, traditional_screenplay


# ------------------------------------------------------------------------------
# Pythonic Screenplay Actor Builder
# ------------------------------------------------------------------------------

def init_actor():
  return Actor(ask_question, call_interaction, traditional_screenplay)
