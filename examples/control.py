from spade_bdi.bdi import BDIAgent
from spade.template import Template
from spade.behaviour import PeriodicBehaviour
from datetime import datetime
from spade.agent import Agent


class BossAgent(BDIAgent):
    async def setup(self):
        template = Template(metadata={"performative": "BDI"})
        self.add_behaviour(self.BDIBehaviour(), template)

        template = Template(metadata={"performative": "Modify"})
        self.add_behaviour(self.Modify(
            period=5, start_at=datetime.now()), template)

    class Modify(PeriodicBehaviour):
        async def run(self):
            tipo = self.agent.bdi.get_belief_value("type")[0]
            if tipo == 'inc':
                self.agent.bdi.set_belief('type', 'dec')
            else:
                self.agent.bdi.set_belief('type', 'inc')


b = BDIAgent("slave_1@localhost", "bdisimple", "slave.asl")
b.start()
c = BDIAgent("slave_2@localhost", "bdisimple3", "slave.asl")
c.start()
a = BossAgent("Boss@localhost", "bdiboss", "boss.asl")
a.start()
print("started")
