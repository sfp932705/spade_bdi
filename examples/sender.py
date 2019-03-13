from spade_bdi.bdi import BDIAgent

a = BDIAgent("BDIAgent@localhost", "bditest", "sender.asl")
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
