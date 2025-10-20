from communication_factory import CommunicationFactory
from banking_server import BankingServer
from logical_clock import LamportClock
from priority_queue import PriorityQueue
from balance_table import BalanceTable
from blockchain import BlockChain
from exceptions import Abort
import tkinter as tk
from tkinter import messagebox


class ClientInterface:


    def __init__(self, args, comm_factory: CommunicationFactory, banking_server: BankingServer, lamport_clock: LamportClock, pqueue: PriorityQueue, dictionary: BalanceTable, block_chain: BlockChain):
        self.args = args
        self.comm_factory = comm_factory
        self.banking_server = banking_server
        self.lamport_clock = lamport_clock
        self.pqueue = pqueue
        # self.balance_table = balance_table
        self.dictionary = dictionary
        self.block_chain = block_chain

        self.root = tk.Tk()
        self.root.title(f"Banking Client {lamport_clock.proc_id}")
        self.root.geometry("400x300")

        self.balance_var = tk.StringVar()
        self.balance_var.set(f"Balance: ${self.dictionary}")
        balance_label = tk.Label(self.root, textvariable=self.balance_var)
        balance_label.pack(pady=10)

        tk.Label(self.root, text="Receiver:").pack()
        self.receiver_entry = tk.Entry(self.root)
        self.receiver_entry.pack()

        tk.Label(self.root, text="Amount:").pack()
        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.pack()

        tk.Button(self.root, text="Perform Transaction", command=self.perform_transaction).pack(pady=5)
        tk.Button(self.root, text="Check Balance", command=self.check_balance).pack(pady=5)
        tk.Button(self.root, text="View Blockchain", command=self.show_blockchain).pack(pady=5)
        tk.Button(self.root, text="View Balance Table", command=self.show_balance_table).pack(pady=5)

    def start(self):
        self.root.mainloop()

    def perform_transaction(self):

        try:
            receiver = self.receiver_entry.get()
            if receiver == self.lamport_clock.proc_id:
                raise Exception("Attempt to perform self transfer")
            amount = self.amount_entry.get()
            amount = float(amount)
            self.banking_server.transcation(self.lamport_clock, self.pqueue, self.dictionary, self.block_chain, receiver, amount, self.comm_factory)
            messagebox.showinfo("Success", "Transaction SUCCESS!")
            self.update_balance()
        except ValueError:
            messagebox.showerror("Error", "Invalid amount entered!")
        except Abort:
            messagebox.showerror("Error", "Transaction FAILED!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def check_balance(self):
        balance = self.banking_server.balance_request(self.args.client, self.dictionary)
        messagebox.showinfo("Balance", f"Current Balance: ${balance}")

    def show_blockchain(self):
        messagebox.showinfo("Blockchain", str(self.block_chain))

    def show_balance_table(self):
        messagebox.showinfo("Balance Table", str(self.dictionary))

    def update_balance(self):
        self.balance_var.set(f"Balance: ${self.dictionary}")

    # def client_interface(args, comm_factory: CommunicationFactory, banking_server: BankingServer, lamport_clock: LamportClock, pqueue: PriorityQueue, balance_table: BalanceTable, block_chain: BlockChain):

            
        

        # GUI Setup
        

        # print(f"Balance: ${balance_table[lamport_clock.proc_id]}")
        # while True:
        #     comm_factory.REPLIES.clear()

        #     s = input("Transaction or Balance:\n")
        #     try:

        #         if s == "t":
        #             receiver = input("Transaction Receiver:\n")
        #             amount = input("Transaction Amount:\n")
        #             banking_server.transcation(lamport_clock, pqueue, balance_table, block_chain, receiver, float(amount), comm_factory)
        #             print("Transaction SUCCESS!")
        #         elif s == "b":
        #             balance = banking_server.balance_request(args.client, balance_table)
        #             print("Current Balance is: {}".format(balance))
        #         elif s == "bl":
        #             print("Current Block Chain Information is: ")
        #             print(block_chain)
        #         elif s == "bt":
        #             print("Current Balance table is: ")
        #             print(balance_table)
        #         else:
        #             continue

        #     except Abort as e:
        #         print("Transaction FAILED!")

        #     except Exception as e:
        #         print(e)
        #         raise Exception("Runtime Error!")
