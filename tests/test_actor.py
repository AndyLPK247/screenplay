"""
This module contains unit tests for the Actor class.
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

import pytest
import sys

from collections import OrderedDict
from screenplay.actor.actor import Actor
from screenplay.actor.builders import init_actor
from screenplay.actor.exceptions import UnknowableArgumentError, MissingParameterError, UnknownSayingError
# from screenplay.actor import wait, on, to
from screenplay.pattern import *


# ------------------------------------------------------------------------------
# Fixtures
# ------------------------------------------------------------------------------

@pytest.fixture
def actor():
  """Creates an Actor instance with an empty context."""
  return Actor()


@pytest.fixture
def pythonic_actor():
  """Creates an Actor instance with the full Pythonic context."""
  return init_actor()


# ------------------------------------------------------------------------------
# Pattern Functions
# ------------------------------------------------------------------------------

@ability
def be_cool():
  return {'cool': True}


@ability
def go_super_saiyan(extra):
  return {'hair': 'blonde', 'power': 9001, 'extra': extra}


@condition
def be(actual, value):
  return actual == value


@condition
def contain(actual, value):
  return value in actual


@condition
def assume_bool(a=1, b=1):
  return a == b


@interaction
def do_it(task, speed):
  return f"{task} at {speed} speed"


@interaction
def whip_it_good():
  return True


@interaction
def assume_things(a=1, b=2):
  return a + b


@saying
def try_things(actor, name):
  if len(name) > 1:
    def try_it():
      return f"tried {name}"
    return try_it


@saying
def shout(actor, name):
  if name == "shout":
    def out_loud(words):
      return words.upper()
    return out_loud


def noop():
  pass


# ------------------------------------------------------------------------------
# Pattern Assertion Functions
# ------------------------------------------------------------------------------

def assert_abilities(actor):
  assert len(actor.abilities) == 2
  assert actor.abilities['be_cool'] == be_cool
  assert actor.abilities['go_super_saiyan'] == go_super_saiyan


def assert_conditions(actor):
  assert len(actor.conditions) == 3
  assert actor.conditions['be'] == be
  assert actor.conditions['contain'] == contain
  assert actor.conditions['assume_bool'] == assume_bool


def assert_interactions(actor):
  assert len(actor.interactions) == 3
  assert actor.interactions['assume_things'] == assume_things
  assert actor.interactions['do_it'] == do_it
  assert actor.interactions['whip_it_good'] == whip_it_good


def assert_sayings(actor):
  assert len(actor.sayings) == 2
  assert actor.sayings['try_things'] == try_things
  assert actor.sayings['shout'] == shout


def assert_all_functions(actor):
  assert_abilities(actor)
  assert_conditions(actor)
  assert_interactions(actor)
  assert_sayings(actor)


# ------------------------------------------------------------------------------
# Tests for Knowing Traits
# ------------------------------------------------------------------------------

@pytest.mark.parametrize(
  "attr",
  ['abilities', 'conditions', 'interactions', 'sayings', 'traits'])
def test_initial_actor_is_empty(actor, attr):
  attr_dict = getattr(actor, attr)
  assert isinstance(attr_dict, OrderedDict)
  assert len(attr_dict) == 0


@pytest.mark.parametrize(
  "key,value",
  [
    ("number", 3.14),
    ("string", "Hello, World!"),
    ("boolean", False),
    ("list", [1, 2, 3]),
    ("set", {1, 2, 3}),
    ("dict", {'a': 1, 'b': 2}),
    ("object", object())
  ]
)
def test_actor_knows_a_trait(actor, key, value):
  traits = {key: value}
  actor.knows(**traits)
  assert len(actor.traits) == 1
  assert actor.traits[key] == value


def test_actor_knows_multiple_traits_with_one_call_each(actor):
  actor.knows(a=1)
  actor.knows(b=2)
  actor.knows(c=3)
  assert len(actor.traits) == 3
  assert actor.traits['a'] == 1
  assert actor.traits['b'] == 2
  assert actor.traits['c'] == 3


def test_actor_knows_multiple_traits_with_one_call_for_all(actor):
  actor.knows(a=1, b=2, c=3)
  assert len(actor.traits) == 3
  assert actor.traits['a'] == 1
  assert actor.traits['b'] == 2
  assert actor.traits['c'] == 3


def test_actor_knows_traits_in_order(actor):
  actor.knows(e=5, d=4, c=3, b=2, a=1)
  assert list(actor.traits.keys()) == ['e', 'd', 'c', 'b', 'a']


def test_actor_knows_traits_being_overridden(actor):
  actor.knows(a=1, b=2, c=3)
  actor.knows(b=99)
  assert actor.traits['b'] == 99


# ------------------------------------------------------------------------------
# Tests for Knowing Abilities
# ------------------------------------------------------------------------------

def test_actor_knows_an_ability(actor):
  actor.knows(be_cool)
  assert len(actor.abilities) == 1
  assert actor.abilities['be_cool'] == be_cool


def test_actor_knows_multiple_abilities_with_one_call_each(actor):
  actor.knows(be_cool)
  actor.knows(go_super_saiyan)
  assert_abilities(actor)


def test_actor_knows_multiple_abilities_with_one_call_for_all(actor):
  actor.knows(be_cool, go_super_saiyan)
  assert_abilities(actor)


def test_actor_knows_abilities_in_order(actor):
  actor.knows(go_super_saiyan, be_cool)
  assert list(actor.abilities.keys()) == ['go_super_saiyan', 'be_cool']


def test_actor_knows_a_duplicate_ability(actor):
  actor.knows(be_cool, go_super_saiyan)
  actor.knows(be_cool)
  assert_abilities(actor)


# ------------------------------------------------------------------------------
# Tests for Knowing Conditions
# ------------------------------------------------------------------------------

def test_actor_knows_a_condition(actor):
  actor.knows(be)
  assert len(actor.conditions) == 1
  assert actor.conditions['be'] == be


def test_actor_knows_multiple_conditions_with_one_call_each(actor):
  actor.knows(be)
  actor.knows(contain)
  actor.knows(assume_bool)
  assert_conditions(actor)


def test_actor_knows_multiple_conditions_with_one_call_for_all(actor):
  actor.knows(be, contain, assume_bool)
  assert_conditions(actor)


def test_actor_knows_conditions_in_order(actor):
  actor.knows(contain, be)
  assert list(actor.conditions.keys()) == ['contain', 'be']


def test_actor_knows_a_duplicate_condition(actor):
  actor.knows(be, contain, assume_bool)
  actor.knows(be)
  assert_conditions(actor)


# ------------------------------------------------------------------------------
# Tests for Knowing Interactions
# ------------------------------------------------------------------------------

def test_actor_knows_an_interaction(actor):
  actor.knows(do_it)
  assert len(actor.interactions) == 1
  assert actor.interactions['do_it'] == do_it


def test_actor_knows_a_task(actor):
  @task
  def some_task():
    pass

  actor.knows(some_task)
  assert len(actor.interactions) == 1
  assert actor.interactions['some_task'] == some_task


def test_actor_knows_a_question(actor):
  @question
  def some_question():
    return "answered"

  actor.knows(some_question)
  assert len(actor.interactions) == 1
  assert actor.interactions['some_question'] == some_question


def test_actor_knows_multiple_interactions_with_one_call_each(actor):
  actor.knows(do_it)
  actor.knows(whip_it_good)
  actor.knows(assume_things)
  assert_interactions(actor)


def test_actor_knows_multiple_interactions_with_one_call_for_all(actor):
  actor.knows(do_it, whip_it_good, assume_things)
  assert_interactions(actor)


def test_actor_knows_interactions_in_order(actor):
  actor.knows(whip_it_good, do_it)
  assert list(actor.interactions.keys()) == ['whip_it_good', 'do_it']


def test_actor_knows_a_duplicate_interaction(actor):
  actor.knows(do_it, whip_it_good, assume_things)
  actor.knows(do_it)
  assert_interactions(actor)


# ------------------------------------------------------------------------------
# Tests for Knowing Sayings
# ------------------------------------------------------------------------------

def test_actor_knows_a_saying(actor):
  actor.knows(try_things)
  assert len(actor.sayings) == 1
  assert actor.sayings['try_things'] == try_things


def test_actor_knows_multiple_sayings_with_one_call_each(actor):
  actor.knows(try_things)
  actor.knows(shout)
  assert_sayings(actor)


def test_actor_knows_multiple_sayings_with_one_call_for_all(actor):
  actor.knows(try_things, shout)
  assert_sayings(actor)


def test_actor_knows_sayings_in_order(actor):
  actor.knows(shout, try_things)
  assert list(actor.sayings.keys()) == ['shout', 'try_things']


def test_actor_knows_a_duplicate_saying(actor):
  actor.knows(try_things, shout)
  actor.knows(try_things)
  assert_sayings(actor)


# ------------------------------------------------------------------------------
# Tests for Knowing Multiple Types
# ------------------------------------------------------------------------------

def test_actor_knows_multiple_types_with_one_call(actor):
  actor.knows(be_cool, go_super_saiyan, be, contain, assume_bool, do_it, 
    whip_it_good, assume_things, try_things, shout)
  assert_all_functions(actor)


# ------------------------------------------------------------------------------
# Tests for Knowing Modules
# ------------------------------------------------------------------------------

def test_actor_knows_module(actor):
  actor.knows(sys.modules[__name__])
  assert_all_functions(actor)


# ------------------------------------------------------------------------------
# Tests for Knowing Other Actors
# ------------------------------------------------------------------------------

def test_actor_knows_another_actor(actor):
  other = Actor()
  other.knows(be_cool, go_super_saiyan, be, contain, assume_bool, do_it, 
    whip_it_good, assume_things, try_things, shout)
  actor.knows(other)
  assert_all_functions(actor)


# ------------------------------------------------------------------------------
# Tests for Attempting to Know Non-Screenplay Items
# ------------------------------------------------------------------------------

def test_actor_cannot_know_an_arbitrary_function(actor):
  with pytest.raises(UnknowableArgumentError):
    actor.knows(noop)


def test_actor_cannot_know_an_arbitrary_object(actor):
  obj = object()
  with pytest.raises(UnknowableArgumentError):
    actor.knows(obj)


def test_actor_cannot_know_an_arbitrary_list(actor):
  stuff = list((1, 2, 3))
  with pytest.raises(UnknowableArgumentError):
    actor.knows(stuff)


def test_actor_cannot_know_an_arbitrary_set(actor):
  stuff = set((1, 2, 3))
  with pytest.raises(UnknowableArgumentError):
    actor.knows(stuff)


def test_actor_cannot_know_an_arbitrary_dict(actor):
  stuff = dict(a=1, b=2, c=3)
  with pytest.raises(UnknowableArgumentError):
    actor.knows(stuff)


# ------------------------------------------------------------------------------
# Tests for Having Abilities
# ------------------------------------------------------------------------------

def test_actor_can_do_ability_without_args(actor):
  actor.can(be_cool)
  assert len(actor.traits) == 1
  assert actor.traits['cool'] == True


def test_actor_can_do_ability_with_args(actor):
  actor.can(go_super_saiyan, extra='yes')
  assert len(actor.traits) == 3
  assert actor.traits['hair'] == 'blonde'
  assert actor.traits['power'] == 9001
  assert actor.traits['extra'] == 'yes'


def test_actor_cannot_do_non_ability(actor):
  with pytest.raises(NotAbilityError):
    actor.can(noop)


# ------------------------------------------------------------------------------
# Tests for Calling Interactions
# ------------------------------------------------------------------------------

def test_actor_calls_interaction_without_parameters(actor):
  response = actor.call(whip_it_good)
  assert response


def test_actor_calls_interaction_with_args_and_without_traits(actor):
  response = actor.call(do_it, task="program", speed="lightning")
  assert response == "program at lightning speed"


def test_actor_calls_interaction_without_args_and_with_traits(actor):
  actor.knows(task="program", speed="lightning")
  response = actor.call(do_it)
  assert response == "program at lightning speed"


def test_actor_calls_interaction_with_both_args_and_traits(actor):
  actor.knows(task="program")
  response = actor.call(do_it, speed="lightning")
  assert response == "program at lightning speed"


def test_actor_calls_interaction_with_args_that_override_traits(actor):
  actor.knows(task="program", speed="lightning")
  response = actor.call(do_it, task="drive")
  assert response == "drive at lightning speed"


def test_actor_calls_interaction_with_unnecessary_args_that_are_ignored(actor):
  response = actor.call(do_it, task="program", speed="lightning", garbage=True)
  assert response == "program at lightning speed"


def test_actor_calls_interaction_with_unnecessary_traits_that_are_ignored(actor):
  actor.knows(garbage=True)
  response = actor.call(do_it, task="program", speed="lightning")
  assert response == "program at lightning speed"


def test_actor_calls_interaction_with_default_parameters(actor):
  response = actor.call(assume_things)
  assert response == 3


def test_actor_calls_interaction_with_args_and_default_parameters(actor):
  response = actor.call(assume_things, b=9)
  assert response == 10


def test_actor_calls_interaction_with_missing_parameters(actor):
  with pytest.raises(MissingParameterError):
    actor.call(do_it)


def test_actor_calls_interaction_with_an_actor_parameter(actor):
  @interaction
  def get_actor(actor):
    return actor
  
  response = actor.call(get_actor)
  assert response == actor


def test_actor_calls_a_non_interaction(actor):
  with pytest.raises(NotInteractionError):
    actor.call(noop)


# ------------------------------------------------------------------------------
# Tests for Checking Conditions
# ------------------------------------------------------------------------------

def test_actor_checks_condition_without_parameters_to_be_true(actor):
  @condition
  def always_true():
    return True
  
  response = actor.check(always_true)
  assert response == True


def test_actor_checks_condition_without_parameters_to_be_false(actor):
  @condition
  def always_false():
    return False
  
  response = actor.check(always_false)
  assert response == False


def test_actor_checks_condition_with_args_and_without_traits(actor):
  response = actor.check(be, actual=4, value=4)
  assert response == True


def test_actor_checks_condition_without_args_and_with_traits(actor):
  actor.knows(actual="hi", value="hi")
  response = actor.check(be)
  assert response == True


def test_actor_checks_condition_with_both_args_and_traits(actor):
  actor.knows(actual="hi")
  response = actor.check(be, value="hi")
  assert response == True


def test_actor_checks_condition_with_args_that_override_traits(actor):
  actor.knows(actual=99, value=99)
  response = actor.check(be, value=2)
  assert response == False


def test_actor_checks_condition_with_unnecessary_args_that_are_ignored(actor):
  response = actor.check(be, actual=4, value=4, garbage="bo-ha-ha")
  assert response == True


def test_actor_checks_condition_with_unnecessary_traits_that_are_ignored(actor):
  actor.knows(actual=99, value=99, garbage="stuff")
  response = actor.check(be)
  assert response == True


def test_actor_checks_condition_with_default_parameters(actor):
  response = actor.check(assume_bool)
  assert response == True


def test_actor_checks_condition_with_args_and_default_parameters(actor):
  response = actor.check(assume_bool, b=2)
  assert response == False


def test_actor_checks_condition_with_missing_parameters(actor):
  with pytest.raises(MissingParameterError):
    actor.check(be)


def test_actor_checks_condition_with_an_actor_parameter(actor):
  @condition
  def has_actor(actor):
    return actor is not None
  
  response = actor.check(has_actor)
  assert response == True


def test_actor_checks_a_non_condition(actor):
  with pytest.raises(NotConditionError):
    actor.check(noop)


# ------------------------------------------------------------------------------
# Tests for Calling Sayings
# ------------------------------------------------------------------------------

def test_actor_getattr_matches_saying(actor):
  actor.knows(shout)
  response = actor.shout("yay")
  assert response == "YAY"


def test_actor_getattr_matches_first_of_multiple_sayings(actor):
  actor.knows(shout, try_things)
  response = actor.shout("yay")
  assert response == "YAY"


def test_actor_getattr_does_not_match_saying(actor):
  actor.knows(shout, try_things)
  with pytest.raises(UnknownSayingError):
    actor.a("stuff")


def test_actor_getattr_does_not_have_sayings(actor):
  with pytest.raises(UnknownSayingError):
    actor.shout("yay")


# ------------------------------------------------------------------------------
# Tests for Calling Abilities via "can_" Sayings
# ------------------------------------------------------------------------------

def test_actor_can_do_ability_without_args_via_saying(pythonic_actor):
  pythonic_actor.knows(be_cool)
  pythonic_actor.can_be_cool()
  assert len(pythonic_actor.traits) == 1
  assert pythonic_actor.traits['cool'] == True


def test_actor_can_do_ability_with_args_via_saying(pythonic_actor):
  pythonic_actor.knows(go_super_saiyan)
  pythonic_actor.can_go_super_saiyan(extra='yes')
  assert len(pythonic_actor.traits) == 3
  assert pythonic_actor.traits['hair'] == 'blonde'
  assert pythonic_actor.traits['power'] == 9001
  assert pythonic_actor.traits['extra'] == 'yes'


def test_actor_cannot_do_unknown_ability_via_saying(pythonic_actor):
  pythonic_actor.knows(go_super_saiyan)
  with pytest.raises(UnknownSayingError):
    pythonic_actor.can_be_cool()


def test_actor_cannot_do_non_ability_via_saying(pythonic_actor):
  with pytest.raises(UnknownSayingError):
    pythonic_actor.can_noop()


# ------------------------------------------------------------------------------
# Tests for Calling Interactions via Direct Sayings
# ------------------------------------------------------------------------------

def test_actor_calls_interaction_without_parameters_via_saying(pythonic_actor):
  pythonic_actor.knows(whip_it_good)
  response = pythonic_actor.whip_it_good()
  assert response


def test_actor_calls_interaction_with_args_and_without_traits_via_saying(pythonic_actor):
  pythonic_actor.knows(do_it)
  response = pythonic_actor.do_it(task="program", speed="lightning")
  assert response == "program at lightning speed"


def test_actor_calls_interaction_without_args_and_with_traits_via_saying(pythonic_actor):
  pythonic_actor.knows(do_it)
  pythonic_actor.knows(task="program", speed="lightning")
  response = pythonic_actor.do_it()
  assert response == "program at lightning speed"


def test_actor_calls_interaction_with_both_args_and_traits_via_saying(pythonic_actor):
  pythonic_actor.knows(do_it)
  pythonic_actor.knows(task="program")
  response = pythonic_actor.do_it(speed="lightning")
  assert response == "program at lightning speed"


def test_actor_calls_interaction_with_args_that_override_traits_via_saying(pythonic_actor):
  pythonic_actor.knows(do_it)
  pythonic_actor.knows(task="program", speed="lightning")
  response = pythonic_actor.do_it(task="drive")
  assert response == "drive at lightning speed"


def test_actor_calls_interaction_with_unnecessary_args_that_are_ignored_via_saying(pythonic_actor):
  pythonic_actor.knows(do_it)
  response = pythonic_actor.do_it(task="program", speed="lightning", garbage=True)
  assert response == "program at lightning speed"


def test_actor_calls_interaction_with_unnecessary_traits_that_are_ignored_via_saying(pythonic_actor):
  pythonic_actor.knows(do_it)
  pythonic_actor.knows(garbage=True)
  response = pythonic_actor.do_it(task="program", speed="lightning")
  assert response == "program at lightning speed"


def test_actor_calls_interaction_with_default_parameters_via_saying(pythonic_actor):
  pythonic_actor.knows(assume_things)
  response = pythonic_actor.assume_things()
  assert response == 3


def test_actor_calls_interaction_with_args_and_default_parameters_via_saying(pythonic_actor):
  pythonic_actor.knows(assume_things)
  response = pythonic_actor.assume_things(b=9)
  assert response == 10


def test_actor_calls_interaction_with_missing_parameters_via_saying(pythonic_actor):
  pythonic_actor.knows(do_it)
  with pytest.raises(MissingParameterError):
    pythonic_actor.do_it()


def test_actor_calls_interaction_with_an_actor_parameter_via_saying(pythonic_actor):
  @interaction
  def get_actor(actor):
    return actor
  
  pythonic_actor.knows(get_actor)
  response = pythonic_actor.get_actor()
  assert response == pythonic_actor


def test_actor_calls_a_non_interaction_via_saying(pythonic_actor):
  with pytest.raises(UnknownSayingError):
    pythonic_actor.noop()


# ------------------------------------------------------------------------------
# Tests for Asking Questions via "get_"
# ------------------------------------------------------------------------------

def test_actor_gets_an_answer_to_a_question_via_saying(pythonic_actor):
  @question
  def greeting(name):
    return f'Hello, {name}!'

  pythonic_actor.knows(greeting)
  response = pythonic_actor.get_greeting(name='Andy')
  assert response == 'Hello, Andy!'


def test_actor_asks_a_non_question_via_saying(pythonic_actor):
  with pytest.raises(UnknownSayingError):
    pythonic_actor.get_noop()


# ------------------------------------------------------------------------------
# Tests for Calling Tasks via "attempts_to"
# ------------------------------------------------------------------------------

def test_actor_attempts_to_do_a_task(pythonic_actor):
  saved = 0

  @task
  def do_stuff(value):
    nonlocal saved
    saved = value

  pythonic_actor.attempts_to(do_stuff, value = 1)
  assert saved == 1


def test_actor_attempts_to_do_an_interaction(pythonic_actor):
  with pytest.raises(NotTaskError):
    pythonic_actor.attempts_to(do_it)


def test_actor_attempts_to_do_a_raw_function(pythonic_actor):
  with pytest.raises(NotTaskError):
    pythonic_actor.attempts_to(noop)


# ------------------------------------------------------------------------------
# Tests for Calling Questions via "asks_for"
# ------------------------------------------------------------------------------

def test_actor_asks_for_a_question(pythonic_actor):
  @question
  def some_info(value):
    return value
  
  answer = pythonic_actor.asks_for(some_info, value=True)
  assert answer


def test_actor_asks_for_an_interaction(pythonic_actor):
  with pytest.raises(NotQuestionError):
    pythonic_actor.asks_for(do_it)


def test_actor_asks_for_a_raw_function(pythonic_actor):
  with pytest.raises(NotQuestionError):
    pythonic_actor.asks_for(noop)


# ------------------------------------------------------------------------------
# Tests for Wait Interactions
# ------------------------------------------------------------------------------

# def test_wait_with_default_args(actor):
#   wait_actor = wait(actor)
#   assert wait_actor.traits['timeout'] == 30
#   assert wait_actor.traits['interval'] == 1


# def test_wait_with_explicit_args(actor):
#   wait_actor = wait(actor, timeout=15, interval=0)
#   assert wait_actor.traits['timeout'] == 15
#   assert wait_actor.traits['interval'] == 0


# on: question without args
# on: question with args
# on: non-question
# to: condition without args
# to: condition with args
# to: non-condition
# to: success with no need to wait
# to: success after waiting
# to: no success after waiting (explicit timeout and interval)
# chain: actor.attempts_to(wait, timeout=30, interval=1).on(question, **).to(condition, **)
# chain: actor.attempts_to(wait, timeout=30, interval=1).on(question).to(condition)
# chain: actor.wait(timeout=30, interval=1).on(question).to(question)
# chain: actor.wait().on(question).to(question)


# Test Pythonic Wait Interactions

# on_question: success without parameters
# on_question: success with args only
# on_question: success with args and traits
# on_question: success with extra args
# on_question: DNE
# wait_on_question: success
# wait_on_question: DNE
# to_condition: success without parameters
# to_condition: success with args only
# to_condition: success with args and traits
# to_condition: success with extra args
# to_condition: DNE

# actor.wait().on_question().to_condition()
# actor.wait_on_question().to_condition()
# actor.wait_on_something(locator=SOME_ELEMENT).to_be(value=789)


# Future Tests?

# actor.wait_on_something(locator=SOME_ELEMENT).to_be(789)
# actor.wait_on_something(locator=SOME_ELEMENT).to_match("regex")
# actor.wait_on_something(locator=SOME_ELEMENT).to_contain_substring("substring")
# actor.wait_on_something(locator=SOME_ELEMENT).to_contain("a", "b", "c")
