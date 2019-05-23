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
from screenplay.actor.wait import wait, wait_on_question


# ------------------------------------------------------------------------------
# Pythonic Screenplay Actor Builder
# ------------------------------------------------------------------------------

def init_actor():
  actor = Actor()
  actor.knows(call_ability, ask_question, call_interaction, traditional_screenplay)
  actor.knows(wait, wait_on_question)
  return actor
