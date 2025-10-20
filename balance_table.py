class BalanceTable:

    def __init__(self, default_balance: float):
        self.balance_table: dict[int: float] = {
            1: default_balance,
            2: default_balance,
            3: default_balance
        } 
    
    def __getitem__(self, index: int):
        return self.balance_table[index]
    
    def __setitem__(self, index: int, value: float):
        self.balance_table[index] = value 

    def __repr__(self):
        return f"""Balance Table
                Client 1: ${self.balance_table[1]},
                Client 2: ${self.balance_table[2]},
                Client 3: ${self.balance_table[3]}
               """
    

class Dictionary:

    def __init__(self):
        self.dictionary = {}

    def __getitem__(self, index: int):
        return self.dictionary[index]
    
    def __setitem__(self, index: int, value: float):
        self.dictionary[index] = value 

    def __repr__(self):
        return f"""Dictionary: {self.dictionary}"""
    
