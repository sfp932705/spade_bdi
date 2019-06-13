import argparse

from spade_bdi.bdi import BDIAgent

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='spade bdi master-server example')
    parser.add_argument('--server', type=str, default="localhost", help='XMPP server address.')
    parser.add_argument('--password', type=str, default="bdipassword", help='XMPP password for the agents.')
    args = parser.parse_args()

    a = BDIAgent("BDISenderAgent@" + args.server, args.password, "sender.asl")
    a.bdi.set_belief("receiver", "BDIReceiverAgent@" + args.server)
    a.start()
