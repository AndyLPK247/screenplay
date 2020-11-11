"""
This module contains classes and functions for handling phrases.
A "phrase" is a textual string an actor uses to call a callable.
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

import re

from screenplay.core.actor import Actor


# ------------------------------------------------------------------------------
# Phrase Class
# ------------------------------------------------------------------------------

class Phrase:
  def __init__(self, text):
    self.text = text
  
  def convert_args(self, call_token, **kwargs):
    inlines = self.parse_inline_args(call_token)
    converted = dict()
    converted.update(inlines)
    converted.update(kwargs)
    return converted
    
  def get_regex_pattern(self):
    pattern = re.sub(r'\[(\w+)\]', r'(\\w+)', self.text)
    return f'^{pattern}$'

  def parse_inline_arg_names(self):
    return re.findall(r'\[(\w+)\]', self.text)

  def parse_inline_args(self, call_token):
    names = self.parse_inline_arg_names()
    pattern = self.get_regex_pattern()
    args = re.findall(pattern, call_token)
    kwargs = {(n, a) for n, a in zip(names, args)}
    return kwargs
  
  def __str__(self):
    return self.text


class CustomPhrase:
  def __init__(self, pattern, interaction):
    self.pattern = pattern
    self.interaction = interaction
  
  def matches(self, call_token):
    return re.search(self.pattern, call_token)

  def __str__(self):
    return self.pattern


def call_final_phrase(actor, phrase, interaction, call_token, **kwargs):
  next_actor = Actor(actor)
  converted = phrase.convert_args(call_token, **kwargs)
  next_actor.knows(converted)
  next_actor.call(interaction)


def call_middle_phrase(actor, phrase, next_call, call_token, **kwargs):
  next_actor = Actor(actor)
  converted = phrase.convert_args(call_token, **kwargs)
  next_actor.knows(converted)
  