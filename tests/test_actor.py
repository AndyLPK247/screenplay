import pytest

from screenplay.actor import Actor


@pytest.fixture
def actor():
  return Actor()


# Test Actor

# initial actor is empty
# know traits
# know abilities
# know conditions
# know interactions
# know sayings
# know actor
# know module
# know multiple
# know duplicate
# know none of the above
# can ability without args
# can ability with args
# can unknown ability
# can non-ability
# can duplicate traits
# call interaction without parameters
# call interaction without args and no traits
# call interaction with args and no traits
# call interaction without args and with traits
# call interaction with some args and traits
# call interaction with unnecessary traits
# call interaction with unnecessary args
# call interaction with missing parameters
# call interaction with actor parameter
# can unknown interaction
# call non-interaction
# getattr no sayings
# getattr match saying
# getattr unmatched saying
# getattr match first of multiple sayings


# Test Sayings

# call_ability: "can_" success
# call_ability: "can_" DNE
# call_interaction: success without parameters
# call_interaction: success with args only
# call_interaction: success with args and traits
# call_interaction: success with extra args
# call_interaction: DNE
# attempts_to: task
# attempts_to: interaction
# attempts_to: raw function
# asks_for: question
# asks_for: interaction
# asks_for: raw function


# Test Wait Interactions

# wait: defaults
# wait: arg values
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
