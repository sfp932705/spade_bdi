# -*- coding: utf-8 -*-
from spade.behaviour import CyclicBehaviour
import pyson
import pyson.runtime
import pyson.stdlib
import asyncio
from spade.agent import Agent
from spade.template import Template
from spade.message import Message
import json
from ast import literal_eval
from loguru import logger

PERCEPT_TAG = frozenset(
    [pyson.Literal("source", (pyson.Literal("percept"), ))])


class BDIAgent(Agent):
    async def setup(self):
        template = Template(metadata={"performative": "BDI"})
        self.add_behaviour(self.BDIBehaviour(), template)

    def add_behaviour(self, behaviour, template=None):
        if type(behaviour) == self.BDIBehaviour:
            self.bdi = behaviour
        super().add_behaviour(behaviour, template)

    def set_asl(self, asl):
        self.asl_file = asl
        if self.asl_file == None:
            self.bdi_enabled = False
        else:
            with open(self.asl_file) as source:
                self.bdi_agent = self.bdi_env.build_agent(
                    source, self.bdi_actions)
            self.bdi_agent.name = self.jid
            self.bdi_enabled = True

    def set_env(self):
        self.bdi_env = pyson.runtime.Environment()
        self.bdi_actions = pyson.Actions(pyson.stdlib.actions)
        self.bdi.add_actions()

    def __init__(self, jid, password, asl=None, *args, **kwargs):
        self.asl_file = asl
        self.bdi_enabled = False
        super().__init__(jid, password, *args, **kwargs)

    class BDIBehaviour(CyclicBehaviour):
        def add_actions(self):
            @self.agent.bdi_actions.add(".send", 3)
            def _send(agent, term, intention):
                receiver = pyson.grounded(term.args[0], intention.scope)
                ilf = pyson.grounded(term.args[1], intention.scope)
                if not pyson.is_atom(ilf):
                    return
                ilf_type = ilf.functor
                mdata = {"performative": "BDI",
                         "ilf_type": ilf_type, }
                body = json.dumps({"functor": str(term.args[2].functor),
                                   "args": str(term.args[2].args)})
                msg = Message(to=receiver, body=body, metadata=mdata)
                self.agent.submit(self.send(msg))
                yield

            @self.agent.bdi_actions.add(".custom_action", 1)
            def _custom_action(agent, term, intention):
                arg_0 = pyson.grounded(term.args[0], intention.scope)
                print(arg_0)
                yield

            @self.agent.bdi_actions.add_function(".a_function", (int,))
            def _a_function(x):
                return x**4

            @self.agent.bdi_actions.add_function("literal_function", (pyson.Literal,))
            def _literal_function(x):
                return x

        def set_belief(self, name, *args):
            """Set an agent's belief. If it already exists, updates it."""
            new_args = ()
            for x in args:
                if type(x) == str:
                    new_args += (pyson.Literal(x),)
                else:
                    new_args += (x,)
            term = pyson.Literal(name, tuple(new_args), PERCEPT_TAG)
            found = False
            for belief in list(self.agent.bdi_agent.beliefs[term.literal_group()]):
                if pyson.unifies(term, belief):
                    found = True
                else:
                    self.agent.bdi_agent.call(pyson.Trigger.removal, pyson.GoalType.belief, belief,
                                              pyson.runtime.Intention())
            if not found:
                self.agent.bdi_agent.call(pyson.Trigger.addition, pyson.GoalType.belief, term,
                                          pyson.runtime.Intention())

        def remove_belief(self, name, *args):
            """Remove an existing agent's belief."""
            new_args = ()
            for x in args:
                if type(x) == str:
                    new_args += (pyson.Literal(x),)
                else:
                    new_args += (x,)
            term = pyson.Literal(name, tuple(new_args), PERCEPT_TAG)
            self.agent.bdi_agent.call(pyson.Trigger.removal, pyson.GoalType.belief, term,
                                      pyson.runtime.Intention())

        def get_belief(self, key, pyson_format=False):
            """Get an agent's existing belief. The first belief matching
            <key> is returned. Keep <pyson_format> False to strip pyson
            formatting."""
            key = str(key)
            for beliefs in self.agent.bdi_agent.beliefs:
                if beliefs[0] == key:
                    raw_belief = (
                        str(list(self.agent.bdi_agent.beliefs[beliefs])[0]))
                    if ')[source' in raw_belief and not pyson_format:
                        raw_belief = raw_belief.split(
                            '[')[0].replace('"', '')
                    belief = raw_belief
                    return belief
            return None

        def get_belief_value(self, key):
            """Get an agent's existing value or values of the <key> belief. The first belief matching
            <key> is returned"""
            belief = self.get_belief(key)
            if belief:
                return tuple(belief.split('(')[1].split(')')[0].split(','))
            else:
                return None

        def get_beliefs(self, pyson_format=False):
            """Get agent's beliefs.Keep <pyson_format> False to strip pyson
            formatting."""
            belief_list = []
            for beliefs in self.agent.bdi_agent.beliefs:
                try:
                    raw_belief = (
                        str(list(self.agent.bdi_agent.beliefs[beliefs])[0]))
                    if ')[source(' in raw_belief and not pyson_format:
                        raw_belief = raw_belief.split('[')[0].replace('"', '')
                    belief_list.append(raw_belief)
                except IndexError:
                    pass
            return belief_list

        def print_beliefs(self, pyson_format=False):
            """Print agent's beliefs.Keep <pyson_format> False to strip pyson
            formatting."""
            print("PRINTING BELIEFS")
            for beliefs in self.agent.bdi_agent.beliefs.values():
                for belief in beliefs:
                    if ')[source(' in str(belief) and not pyson_format:
                        belief = str(belief).split('[')[0].replace('"', '')
                    print(belief)

        async def on_start(self):
            """
            Coroutine called before the behaviour is started.
            """
            self.agent.set_env()
            if self.agent.asl_file:
                self.agent.set_asl(self.agent.asl_file)
            else:
                logger.info(
                    "Warning: no ASL specified for {}.".format(self.agent.jid))

        async def run(self):
            """
            Coroutine run cyclic.
            """
            if self.agent.bdi_enabled:
                msg = await self.receive(timeout=0.1)
                if msg:
                    received = json.loads(msg.body)
                    mdata = msg.metadata
                    ilf_type = mdata["ilf_type"]
                    if ilf_type == "tell":
                        goal_type = pyson.GoalType.belief
                        trigger = pyson.Trigger.addition
                    elif ilf_type == "untell":
                        goal_type = pyson.GoalType.belief
                        trigger = pyson.Trigger.removal
                    elif ilf_type == "achieve":
                        goal_type = pyson.GoalType.achievement
                        trigger = pyson.Trigger.addition
                    else:
                        raise pyson.PysonError(
                            "unknown illocutionary force: %s" % ilf_type)
                    intention = pyson.runtime.Intention()
                    args = literal_eval(received["args"])

                    if args != tuple():
                        message = pyson.Literal(
                            received["functor"], args)
                    else:
                        message = pyson.Literal(received["functor"])
                    message = pyson.freeze(message, intention.scope, {})
                    tagged_message = message.with_annotation(
                        pyson.Literal("source", (pyson.Literal(str(msg.sender)), )))
                    self.agent.bdi_agent.call(trigger, goal_type,
                                              tagged_message, intention)
                self.agent.bdi_agent.step()

        async def on_end(self):
            """
            Coroutine called after the behaviour is done or killed.
            """
            pass
