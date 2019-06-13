import argparse

from spade_bdi.bdi import BDIAgent
from spade.template import Template
from spade.behaviour import PeriodicBehaviour
from spade.behaviour import TimeoutBehaviour
from datetime import datetime
from datetime import timedelta


class CounterAgent(BDIAgent):
    async def setup(self):
        template = Template(metadata={"performative": "B1"})
        self.add_behaviour(self.Behav1(period=1, start_at=datetime.now()), template)
        template = Template(metadata={"performative": "B2"})
        self.add_behaviour(self.Behav2(period=5, start_at=datetime.now()), template)
        template = Template(metadata={"performative": "B3"})
        self.add_behaviour(self.Behav3(period=10, start_at=datetime.now()), template)
        template = Template(metadata={"performative": "B4"})
        self.add_behaviour(self.Behav4(start_at=datetime.now() + timedelta(seconds=60)), template)

    class Behav1(PeriodicBehaviour):
        async def on_start(self):
            self.counter = self.agent.bdi.get_belief_value("counter")[0]

        async def run(self):
            if self.counter != self.agent.bdi.get_belief_value("counter")[0]:
                self.counter = self.agent.bdi.get_belief_value("counter")[0]
                print(self.agent.bdi.get_belief("counter"))

    class Behav2(PeriodicBehaviour):
        async def run(self):
            self.agent.bdi.set_belief('counter', 0)

    class Behav3(PeriodicBehaviour):
        async def run(self):
            try:
                type = self.agent.bdi.get_belief_value("type")[0]
                if type == 'inc':
                    self.agent.bdi.set_belief('type', 'dec')
                else:
                    self.agent.bdi.set_belief('type', 'inc')
            except Exception as e:
                print("No belief 'type'.")

    class Behav4(TimeoutBehaviour):
        async def run(self):
            self.agent.bdi.remove_belief('type', 'inc')
            self.agent.bdi.remove_belief('type', 'dec')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='spade bdi master-server example')
    parser.add_argument('--server', type=str, default="localhost", help='XMPP server address.')
    parser.add_argument('--password', type=str, default="bdipassword", help='XMPP password for the agents.')
    args = parser.parse_args()

    a = CounterAgent("counter@" + args.server, args.password, "counter.asl")
    a.start()
    import time
    time.sleep(1)
    print("started")
