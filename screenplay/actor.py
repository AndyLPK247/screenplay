import functools
import inspect
import sys
import time

from collections import OrderedDict
from screenplay.pattern import *


# TODO: 'check' condition?
# TODO: condition with *args?
# TODO: Reconsider interaction *args?


# Screenplay Actor

class Actor:
  def __init__(self):
    self._abilities = OrderedDict()
    self._conditions = OrderedDict()
    self._interactions = OrderedDict()
    self._sayings = OrderedDict()
    self._traits = OrderedDict()

  def _add_actor_context(self, actor):
    self._abilities.update(actor.abilities)
    self._conditions.update(actor.conditions)
    self._interactions.update(actor.interactions)
    self._sayings.update(actor.sayings)
    self._traits.update(actor.traits)
  
  def _add_module_members(self, module):
    members = inspect.getmembers(module)
    self._get_members(members, is_ability, self._abilities)
    self._get_members(members, is_condition, self._conditions)
    self._get_members(members, is_interaction, self._interactions)
    self._get_members(members, is_saying, self._sayings)

  def _get_args(self, interaction, arg_dict):
    applicable_args = dict()
    params = inspect.signature(interaction).parameters

    for name, param in params.items():
      if name in arg_dict:
        applicable_args[name] = arg_dict[name]
      elif name in self._traits:
        applicable_args[name] = self._traits[name]
      elif name == 'actor':
        applicable_args['actor'] = self
      elif param.default == inspect.Parameter.empty:
        raise MissingParameterError(name, interaction)
    
    return applicable_args

  def _get_members(self, members, predicate, target):
    for name, f in members:
      if predicate(f):
        target[name] = f

  @property
  def abilities(self):
    return self._abilities

  @property
  def conditions(self):
    return self._conditions

  @property
  def interactions(self):
    return self._interactions

  @property
  def sayings(self):
    return self._sayings

  @property
  def traits(self):
    return self._traits

  def call(self, interaction, **kwargs):
    validate_interaction(interaction)
    applicable_args = self._get_args(interaction, kwargs)
    return interaction(**applicable_args)

  def can(self, ability, **kwargs):
    validate_ability(ability)
    traits = ability(**kwargs)
    self._traits.update(traits)

  def knows(self, *args, **kwargs):
    self._traits.update(kwargs)

    for arg in args:
      if inspect.ismodule(arg):
        self._add_module_members(arg)
      elif isinstance(arg, Actor):
        self._add_actor_context(arg)
      elif is_ability(arg):
        self._abilities[arg.__name__] = arg
      elif is_condition(arg):
        self._conditions[arg.__name__] = arg
      elif is_interaction(arg):
        self._interactions[arg.__name__] = arg
      elif is_saying(arg):
        self._sayings[arg.__name__] = arg
      else:
        raise UnknowableArgumentError(arg)

  def __getattr__(self, attr):
    for name, saying in self._sayings.items():
      call = saying(self, attr)
      if call is not None:
        return call
    raise UnknownSayingError(attr)


# Actor Exceptions

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


# Common Sayings

@saying
def call_ability(actor, name):
  if name.startswith('can_'):
    ability_name = name[4:]
    if ability_name in actor.abilities:
      ability = actor.abilities[ability_name]
      return functools.partial(actor.can, ability)


@saying
def call_interaction(actor, name):
  if name in actor.interactions:
    interaction = actor.interactions[name]
    return functools.partial(actor.call, interaction)


@saying
def traditional_screenplay(actor, name):
  if name == 'attempts_to':
    def attempts_to(task, **kwargs):
      validate_task(task)
      return actor.call(task, **kwargs)
    return attempts_to
  elif name == 'asks_for':
    def asks_for(question, **kwargs):
      validate_question(question)
      return actor.call(question, **kwargs)
    return asks_for


# Wait Interactions

@interaction
def wait(actor, timeout=30, interval=1):
  wait_actor = Actor()
  wait_actor.knows(actor, call_interaction, on, on_question)
  wait_actor.knows(timeout=timeout, interval=interval)
  return wait_actor


@interaction
def on(actor, question, **q_args):
  validate_question(question)
  on_actor = Actor()
  on_actor.knows(actor, call_interaction, to, to_condition)
  on_actor.knows(on_question=question, on_question_args=q_args)
  return on_actor


@interaction
def to(actor, condition, **c_args):
  # TODO: filter args for condition call

  validate_condition(condition)

  timeout = actor.traits.timeout
  interval = actor.traits.timeout
  question = actor.traits.on_question
  q_args = actor.traits.on_question_args

  end = time.monotonic() + timeout
  answer = actor.call(question, **q_args)
  satisfied = condition(answer, **c_args)

  while not satisfied and time.monotonic() < end:
    time.sleep(interval)
    answer = actor.call(question, **q_args)
    satisfied = condition(answer, **c_args)

  if not satisfied:
    raise WaitTimeoutError(timeout, question, q_args, condition, c_args)


# Wait Sayings

@saying
def on_question(actor, name):
  if name.startswith('on_'):
    question_name = name[3:]
    if question_name in actor.interactions:
      question = actor.interactions[question_name]
      return functools.partial(actor.call, on, actor=actor, question=question)


@saying
def wait_on_question(actor, name):
  if name.startswith('wait_on_'):
    wait_actor = wait(actor)
    on_name = name[5:]
    return on_question(wait_actor, on_name)


@saying
def to_condition(actor, name):
  if name.startswith('to_'):
    condition_name = name[3:]
    if condition_name in actor.conditions:
      condition = actor.conditions[condition_name]
      return functools.partial(actor.call, to, actor=actor, condition=condition)


# Wait Exceptions

def _format_call(func, kwargs):
  name = func.__name__
  args = ", ".join([f"{k}={v}" for (k, v) in kwargs.items()])
  call = f'{name}({args})'
  return call


class WaitTimeoutError(Exception):
  def __init__(self, timeout, question, q_args, condition, c_args):
    q = _format_call(question, q_args)
    c = _format_call(condition, c_args)
    seconds = "seconds" if timeout != 1 else "second"
    super().__init__(f'Waiting for "{q}" to "{c}" timed out after {timeout} {seconds}')
    self.timeout = timeout
    self.question = question
    self.q_args = q_args
    self.condition = condition
    self.c_args = c_args


# Pythonic Screenplay Actor

def screenplay_actor():
  actor = Actor()
  actor.knows(call_ability, call_interaction, traditional_screenplay, wait, wait_on_question)
  return actor
