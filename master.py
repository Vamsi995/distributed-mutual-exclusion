import logging
import argparse
import socket
from communication_factory import CommunicationFactory
import threading
import time
from blockchain import InsertOperation, LookupOperation
from utils import object_to_txt

def send_to_client(client_id, message, comm_factory):
    
    client = comm_factory.CLIENTS[client_id - 1]
    client.send(bytes(message, 'utf-8'))
    time.sleep(3)


def run_server(args):

    host = 'localhost'  # Listen on the local machine only
    port = args.port  # Choose a port number
    comm_factory = CommunicationFactory()

    clientsocket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket1.connect((host, 8001))
    comm_factory.CLIENTS.append(clientsocket1)
    print("Connected with {}".format(clientsocket1.getpeername()))

    thread = threading.Thread(target=comm_factory.master_handle, args=(clientsocket1, comm_factory, args))
    thread.start()

    clientsocket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket2.connect((host, 8002))
    comm_factory.CLIENTS.append(clientsocket2)
    print("Connected with {}".format(clientsocket2.getpeername()))

    thread = threading.Thread(target=comm_factory.master_handle, args=(clientsocket2, comm_factory, args))
    thread.start()


    clientsocket3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket3.connect((host, 8003))
    comm_factory.CLIENTS.append(clientsocket3)
    print("Connected with {}".format(clientsocket3.getpeername()))

    thread = threading.Thread(target=comm_factory.master_handle, args=(clientsocket3, comm_factory, args))
    thread.start()


    time.sleep(3)

    with open(f'{args.inputfile}', 'r') as f:
        lines = f.readlines()

        for line in lines:
    
            out = line.split(" ")

            if len(out) == 4:
                operation, perm, grade, client_id = out
                message = "INSERT_OP" + "|" + object_to_txt(InsertOperation(perm, grade))
                logging.info(f"[Event - INSERT] [PERM - {perm}] [GRADE - {grade}] - [Sent to Client {client_id}]")

                send_to_client(int(client_id), message, comm_factory)
            
            elif len(out) == 3:
                operation, perm, client_id = out
                message = "LOOKUP_OP" + "|" + object_to_txt(LookupOperation(perm))
                logging.info(f"[Event - LOOKUP] [PERM - {perm}] - [Sent to Client {client_id}]")
                send_to_client(int(client_id), message, comm_factory)
            
            elif len(out) == 2:
                operation, id = out
                if operation == "dictionary":
                    message = "DICTIONARY_OP" + "|" + id
                    logging.info(f"[Event - DICTIONARY] - [Sent to Client {id}]")
                    send_to_client(int(id), message, comm_factory)
                elif operation == "wait":
                    logging.info(f"[Event - WAIT] [TIME - {id}]")
                    time.sleep(int(id))








if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    # %(asctime)s - %(levelname)s - 
    parser = argparse.ArgumentParser()
    parser.add_argument('-port', type=int, default=8000)
    parser.add_argument('-inputfile', type=str, default=None)
    parser.add_argument('-outputfile', type=str, default=None)
    args = parser.parse_args()
    run_server(args)





