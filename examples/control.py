from spade_bdi.bdi import BDIAgent
from spade.template import Template
from spade.behaviour import PeriodicBehaviour
from spade.behaviour import TimeoutBehaviour
from datetime import datetime
from datetime import timedelta
from spade.agent import Agent


class MasterAgent(BDIAgent):
    async def setup(self):
        template = Template(metadata={"performative": "BDI"})
        self.add_behaviour(self.BDIBehaviour(), template)

        template = Template(metadata={"performative": "Modify"})
        self.add_behaviour(self.Modify(
            period=5, start_at=datetime.now()), template)

        template = Template(metadata={"performative": "Ending"})
        self.add_behaviour(self.Behav4(
            start_at=datetime.now() + timedelta(seconds=11)), template)

    class Modify(PeriodicBehaviour):
        async def run(self):
            if self.agent.bdi_enabled:
                try:
                    tipo = self.agent.bdi.get_belief_value("tipo")[0]
                    if tipo == 'inc':
                        self.agent.bdi.set_belief('tipo', 'dec')
                    else:
                        self.agent.bdi.set_belief('tipo', 'inc')
                except Exception as e:
                    self.kill()

    class Behav4(TimeoutBehaviour):
        async def run(self):
            self.agent.bdi.remove_belief('tipo', 'inc')
            self.agent.bdi.remove_belief('tipo', 'dec')


import time

b = BDIAgent("slave_1@localhost", "bdisimple", "slave.asl")
future = b.start()
future.result()

c = BDIAgent("slave_2@localhost", "bdisimple3")
future = c.start()
future.result()

a = MasterAgent("master@localhost", "bdimaster")
future = a.start()
future.result()
a.set_asl("master.asl")
a.bdi.set_belief('tipo', 'dec')

time.sleep(5)
print("Enabling BDI for slave2")
c.set_asl("slave.asl")
time.sleep(5)
print("Disabling BDI for slave2")
c.set_asl(None)
