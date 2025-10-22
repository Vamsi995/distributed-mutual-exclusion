import socket
import argparse
import threading
from logical_clock import LamportClock
from priority_queue import PriorityQueue
from blockchain import BlockChain
from balance_table import BalanceTable, Dictionary
from banking_server import BankingServer
from communication_factory import CommunicationFactory
from interface import ClientInterface
import logging

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


    clientsocket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket1.connect((host, 8001))
    comm_factory.CLIENTS.append(clientsocket1)
    print("Connected with {}".format(clientsocket1.getpeername()))

    thread = threading.Thread(target=comm_factory.handle, args=(clientsocket1, pqueue, block_chain, dictionary, comm_factory, lamport_clock, client_interface))
    thread.start()

    clientsocket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket2.connect((host, 8002))
    comm_factory.CLIENTS.append(clientsocket2)
    print("Connected with {}".format(clientsocket2.getpeername()))

    thread = threading.Thread(target=comm_factory.handle, args=(clientsocket2, pqueue, block_chain, dictionary, comm_factory, lamport_clock, client_interface))
    thread.start()

     # Starting Server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    print("Listening on port: {}".format(port))

    limit = 1
    comm_factory.receive(server, pqueue, block_chain, dictionary, limit, lamport_clock, client_interface)
    # client_interface.start()
    
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    parser = argparse.ArgumentParser()
    parser.add_argument('-port', type=int, default=8000)
    parser.add_argument('-client', type=int, default=None)
    parser.add_argument('-balance', type=float, default=10.0)
    args = parser.parse_args()
    run_server(args)