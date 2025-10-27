import socket
import argparse
from logical_clock import LamportClock
from blockchain import BlockChain
from balance_table import BalanceTable, Dictionary
from priority_queue import PriorityQueue
import logging
from banking_server import BankingServer
from communication_factory import CommunicationFactory
from exceptions import Abort
from interface import ClientInterface


def run_server(args):
    host = 'localhost'  # Listen on the local machine only
    port = args.port  # Choose a port number
    lamport_clock = LamportClock(args.client)
    block_chain = BlockChain()
    balance_table = BalanceTable(args.balance)
    dictionary = Dictionary()
    pqueue = PriorityQueue([])
    banking_server = BankingServer()
    comm_factory = CommunicationFactory()
    client_interface = ClientInterface(args, comm_factory, banking_server, lamport_clock, pqueue, dictionary, block_chain)
    limit = 2

    # Starting Server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    print("Listening on port: {}".format(port))

    comm_factory.receive(server, pqueue, block_chain, dictionary, limit, lamport_clock, client_interface)
    client_interface.start()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    # %(asctime)s - %(levelname)s - 
    parser = argparse.ArgumentParser()
    parser.add_argument('-port', type=int, default=8000)
    parser.add_argument('-client', type=int, default=None)
    parser.add_argument('-balance', type=float, default=10.0)
    args = parser.parse_args()
    run_server(args)