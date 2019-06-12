from spade_bdi.bdi import BDIAgent
from spade.template import Template
from spade.behaviour import PeriodicBehaviour
from spade.behaviour import TimeoutBehaviour
from datetime import datetime
from datetime import timedelta
from spade.agent import Agent


class CounterAgent(BDIAgent):
    async def setup(self):
        template = Template(metadata={"performative": "BDI"})
        self.add_behaviour(self.BDIBehaviour(), template)
        template = Template(metadata={"performative": "B1"})
        self.add_behaviour(self.Behav1(
            period=1, start_at=datetime.now()), template)
        template = Template(metadata={"performative": "B2"})
        self.add_behaviour(self.Behav2(
            period=5, start_at=datetime.now()), template)
        template = Template(metadata={"performative": "B3"})
        self.add_behaviour(self.Behav3(
            period=10, start_at=datetime.now()), template)
        template = Template(metadata={"performative": "B4"})
        self.add_behaviour(self.Behav4(
            start_at=datetime.now() + timedelta(seconds=60)), template)

    class Behav1(PeriodicBehaviour):
        async def on_start(self):
            self.contador = self.agent.bdi.get_belief_value("contador")[0]

        async def run(self):
            if self.contador != self.agent.bdi.get_belief_value("contador")[0]:
                self.contador = self.agent.bdi.get_belief_value("contador")[
                    0]
                print(self.agent.bdi.get_belief("contador"))

    class Behav2(PeriodicBehaviour):
        async def run(self):
            self.agent.bdi.set_belief('contador', 0)

    class Behav3(PeriodicBehaviour):
        async def run(self):
            try:
                tipo = self.agent.bdi.get_belief_value("tipo")[0]
                if tipo == 'inc':
                    self.agent.bdi.set_belief('tipo', 'dec')
                else:
                    self.agent.bdi.set_belief('tipo', 'inc')
            except Exception as e:
                print("No belief 'tipo'.")

    class Behav4(TimeoutBehaviour):
        async def run(self):
            self.agent.bdi.remove_belief('tipo', 'inc')
            self.agent.bdi.remove_belief('tipo', 'dec')


a = CounterAgent("counter@localhost", "bditest", "counter.asl")
a.start()
import time
time.sleep(1)
print("started")
