import argparse

from spade_bdi.bdi import BDIAgent

parser = argparse.ArgumentParser(description='spade bdi master-server example')
parser.add_argument('--server', type=str, default="localhost", help='XMPP server address.')
parser.add_argument('--password', type=str, default="bdipassword", help='XMPP password for the agents.')
args = parser.parse_args()

a = BDIAgent("BasicAgent@" + args.server, args.password, "basic.asl")
a.start()

import time
time.sleep(1)

a.bdi.set_belief("car", "azul", "big")
a.bdi.print_beliefs()
print("GETTING FIRST CAR BELIEF")
print(a.bdi.get_belief("car"))
a.bdi.print_beliefs()
a.bdi.remove_belief("car", 'azul', "big")
a.bdi.print_beliefs()
print(a.bdi.get_beliefs())
a.bdi.set_belief("car", 'amarillo')
