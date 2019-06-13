import argparse

from spade_bdi.bdi import BDIAgent

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='spade bdi master-server example')
    parser.add_argument('--server', type=str, default="localhost", help='XMPP server address.')
    parser.add_argument('--password', type=str, default="bdipassword", help='XMPP password for the agents.')
    args = parser.parse_args()

    a = BDIAgent("BDIReceiverAgent@" + args.server, args.password, "receiver.asl")
    a.start()

