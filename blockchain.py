from __future__ import annotations
import hashlib

class BlockChain:

    def __init__(self):
        self.block_chain_head = Block("Genesis", "Genesis", 0.0, "0")
        self.block_chain_tail = self.block_chain_head

    def insert(self, sender, receiver, amount) -> Block:
        block = Block(sender, receiver, amount, self.block_chain_tail.current_hash)
        self.block_chain_tail.next = block
        self.block_chain_tail = block

        return block

    def update_head(self, block: Block) -> None:
        self.block_chain_tail.next = block
        block.prev_hash = self.block_chain_tail.current_hash
        self.block_chain_tail = block

    def __repr__(self):
        return f"{self.block_chain_head}"

class Block:

    def __init__(self, sender: str, receiver: str , amount: float, prev_hash: str, next: Block = None):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.prev_hash = prev_hash
        self.next = next
        self.current_hash = self.calculate_hash()
    

    def calculate_hash(self):
        sha = hashlib.sha256()
        sha.update(str(self.sender).encode('utf-8') + 
                   str(self.receiver).encode('utf-8') + 
                   str(self.amount).encode('utf-8') + 
                   str(self.prev_hash).encode('utf-8'))
        return sha.hexdigest()
    
    def __repr__(self):
        return f"|Client<{self.sender}> pays Client<{self.receiver}> ${self.amount}| -> {self.next}"
    


class InsertOperation:

    def __init__(self, id, grade):
        self.id = id
        self.grade = grade 