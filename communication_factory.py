from __future__ import annotations
import threading
from blockchain import Block, BlockChain, InsertOperation, LookupOperation, LookupOutput, InsertOutput
from balance_table import BalanceTable, Dictionary
from priority_queue import PriorityQueue
from utils import txt_to_object, object_to_txt
import logging
import time
from logical_clock import LamportClock

class CommunicationFactory:

    REPLIES = []
    CLIENTS = []
    SUCCESS = []
    MASTER = None


    def broadcast(self, message, lamport_clock: LamportClock, message_type: str):
        for client in self.CLIENTS:
            client.send(bytes(message, "utf-8"))
        
        logging.info(f"[Event - Broadcast - {message_type}] - [Clock - {lamport_clock.logical_time}] - [Sent from Client {lamport_clock.proc_id}]")

    def send_to_master(self, client, message, lamport_clock: LamportClock, message_type: str):
        client.send(bytes(message, "utf-8"))
        logging.info(f"[Event - Master - {message_type}] - [Clock - {lamport_clock.logical_time}] - [Sent from Client {lamport_clock.proc_id}]")

    def master_handle(self, client, comm_factory, args):

        def write_to_file(message):

            with open(f'{args.outputfile}', 'a') as file:
                file.write(f'{str(message)}\n')


        while True:
            try:
                # Broadcasting Messages
                message = client.recv(4096).decode("utf-8")
                message, piggy_back_obj = message.split("|")

                if message == "INSERT_SUCCESS":
                    piggy_back_clock, piggy_back_op = piggy_back_obj.split("#")
                    attached_clock = txt_to_object(piggy_back_clock)
                    insert_output = txt_to_object(piggy_back_op)
                    write_to_file(insert_output)
                    logging.info(f"[Event - INSERT_SUCCESS] - [Clock - {attached_clock.logical_time}] - [Received from Client {attached_clock.proc_id}]")
                
                elif message == "LOOKUP_SUCCESS":
                    piggy_back_clock, piggy_back_op = piggy_back_obj.split("#")
                    attached_clock = txt_to_object(piggy_back_clock)
                    lookup_output = txt_to_object(piggy_back_op)
                    write_to_file(lookup_output)
                    logging.info(f"[Event - LOOKUP_SUCCESS] - [Clock - {attached_clock.logical_time}] - [Received from Client {attached_clock.proc_id}]")

                elif message == "DICTIONARY_SUCCESS":
                    piggy_back_clock, piggy_back_op = piggy_back_obj.split("#")
                    attached_clock = txt_to_object(piggy_back_clock)
                    dictionary = txt_to_object(piggy_back_op)
                    write_to_file(dictionary)
                    logging.info(f"[Event - DICTIONARY] - [Clock - {attached_clock.logical_time}] - [Received from Client {attached_clock.proc_id}]")



            except Exception as e:
                print(e)
                # Removing And Closing Clients
                comm_factory.CLIENTS.remove(client)
                client.close()
                break


    def receive(self, server, pqueue: PriorityQueue, block_chain: BlockChain, dictionary: Dictionary, client_limit, lamport_clock, client_interface):
        curr_clients = []

        while True:
            # Accept Connection
            client, address = server.accept()
            print("Connected with {}".format(client.getpeername()))

            # if len(self.CLIENTS) == client_limit:
            #     if self.MASTER == None:
            #         self.MASTER = client
            #         thread = threading.Thread(target=self.handle, args=(client, pqueue, block_chain, dictionary, self, lamport_clock, client_interface))
            #         thread.start()
            #         # continue
            #         break

            self.CLIENTS.append(client)
            curr_clients.append(client)
            # Start Handling Thread For Client
            if len(curr_clients) - 1 == client_limit:
                    self.MASTER = self.CLIENTS.pop()
                    thread = threading.Thread(target=self.handle, args=(client, pqueue, block_chain, dictionary, self, lamport_clock, client_interface))
                    thread.start()
                    break
            else:
                thread = threading.Thread(target=self.handle, args=(client, pqueue, block_chain, dictionary, self, lamport_clock, client_interface))
                thread.start()






    def handle(self, client, pqueue: PriorityQueue, block_chain: BlockChain, dictionary: Dictionary, comm_factory: CommunicationFactory, lamport_clock: LamportClock, client_interface):
        while True:
            try:
                # Broadcasting Messages
                message = client.recv(4096).decode("utf-8")
                message, piggy_back_obj = message.split("|")

                if message == "REQUEST":
                    attached_clock = txt_to_object(piggy_back_obj)
                    lamport_clock.update_clock(attached_clock.logical_time)
                    logging.info(f"[Event - REQUEST] - [Clock - {lamport_clock.logical_time}] - [Received from Client {attached_clock.proc_id}]")

                    # Add to local queue
                    # lamport_clock()
                    reply_message = "REPLY" + "|" + object_to_txt(lamport_clock)
                    time.sleep(3)
                    client.send(bytes(reply_message, "utf-8"))
                    pqueue.insert(lamport_clock)
                    logging.info(f"[Event - REPLY] - [Clock - {lamport_clock.logical_time}] - [Sent from Client {lamport_clock.proc_id}]")


                elif message == "REPLY":
                    attached_clock = txt_to_object(piggy_back_obj)
                    comm_factory.REPLIES.append(client)
                    # lamport_clock.update_clock(attached_clock.logical_time)
                    logging.info(f"[Event - REPLY] - [Clock - {lamport_clock.logical_time}] - [Received from Client {attached_clock.proc_id}]")


                elif message == "RELEASE":
                    attached_clock = txt_to_object(piggy_back_obj)
                    # lamport_clock.update_clock(attached_clock.logical_time)
                    pqueue.delete(attached_clock.proc_id)
                    logging.info(f"[Event - RELEASE] - [Clock - {lamport_clock.logical_time}] - [Received from Client {attached_clock.proc_id}]")
                    client_interface.update_balance()

                elif message == "BLOCK":
                    piggy_back_clock, piggy_back_block = piggy_back_obj.split("#")
                    attached_clock = txt_to_object(piggy_back_clock)
                    block: Block = txt_to_object(piggy_back_block)
                    # lamport_clock.update_clock(attached_clock.logical_time)
                    block_chain.update_head(block)
                    # balance_table[int(block.sender)] -= block.amount
                    # balance_table[int(block.receiver)] += block.amount
                    logging.info(f"[Event - BLOCK] - [Clock - {lamport_clock.logical_time}] - [Received from Client {attached_clock.proc_id}]")

                elif message == "INSERT":
                    piggy_back_clock, piggy_back_op = piggy_back_obj.split("#")
                    attached_clock = txt_to_object(piggy_back_clock)
                    insert_operation: InsertOperation = txt_to_object(piggy_back_op)
                    id, grade = insert_operation.id, insert_operation.grade
                    dictionary[id] = grade
                    # update your balance based on your data structure
                    logging.info(f"[Event -  INSERT] - [Clock - {lamport_clock.logical_time}] - [Received from Client {attached_clock.proc_id}]")
                    success_message = "SUCCESS" + "|" + object_to_txt(lamport_clock)
                    client.send(bytes(success_message, "utf-8"))

                    
                elif message == "SUCCESS":
                    attached_clock = txt_to_object(piggy_back_obj)
                    logging.info(f"[Event - SUCCESS] - [Clock - {lamport_clock.logical_time}] - [Received from Client {attached_clock.proc_id}]")
                    comm_factory.SUCCESS.append(client)
                    client_interface.update_balance()

                elif message == "INSERT_OP":
                    insert_op = txt_to_object(piggy_back_obj)
                    client_interface.banking_server.transcation(lamport_clock, pqueue, dictionary, block_chain, insert_op.id, insert_op.grade, comm_factory)
                    message = "INSERT_SUCCESS" + "|" + object_to_txt(lamport_clock) + "#" + object_to_txt(InsertOutput(insert_op.id, insert_op.grade, lamport_clock.proc_id))
                    self.send_to_master(client, message, lamport_clock, "INSERT_SUCCESS")
                
                elif message == "LOOKUP_OP":
                    lookup_op = txt_to_object(piggy_back_obj)
                    grade = dictionary[lookup_op.id]
                    # "BLOCK" + "|" + object_to_txt(lamport_clock) + "#" + object_to_txt(block), lamport_clock, "BLOCK"
                    message = "LOOKUP_SUCCESS" + "|" + object_to_txt(lamport_clock) + "#" + object_to_txt(LookupOutput(lookup_op.id, grade))
                    self.send_to_master(client, message, lamport_clock, "LOOKUP_SUCCESS")
                

                elif message == "DICTIONARY_OP":
                    # "BLOCK" + "|" + object_to_txt(lamport_clock) + "#" + object_to_txt(block), lamport_clock, "BLOCK"
                    message = "DICTIONARY_SUCCESS" + "|" + object_to_txt(lamport_clock) + "#" + object_to_txt(dictionary)
                    self.send_to_master(client, message, lamport_clock, "DICTIONARY_SUCCESS")

            except Exception as e:
                print(e)
                # Removing And Closing Clients
                comm_factory.CLIENTS.remove(client)
                client.close()
                break

