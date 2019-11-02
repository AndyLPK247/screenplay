"""
This module contains builders for the Actor class.
The 'init_actor' constructs the standard Pythonic Screenplay Actor.
As a best practice, only use builders to initialize Actor instances.
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

from screenplay.actor.actor import Actor
from screenplay.actor.sayings import call_ability, ask_question, call_interaction, traditional_screenplay


# ------------------------------------------------------------------------------
# Pythonic Screenplay Actor Builder
# ------------------------------------------------------------------------------

def init_actor():
  return Actor(call_ability, ask_question, call_interaction, traditional_screenplay)
