import os
import csv
import json
import time

from hashlib import sha256
from supersecrets import digest

from utils import *

class DatabaseException(Exception): 
    pass

class Database:
    _difficulty        = 4
    _blockchain_file   = "data\\blockchain.json"

    _users_file_name   = "data\\anarchist.json"
    _users_csv_file    = "data\\anarchist.csv"
    _transactions_csv  = "data\\transactions.csv"
    _transactions_file = "data\\transactions.json"

    def log(self, message: str) -> None:
        if self.verbose:
            rgb("[*] " + str(message).replace("[*]", ""), (0, 255, 255))

    def warn(self, message: str) -> None:
        if self.verbose:
            rgb("[*] " + str(message), (255, 255, 0))

    def error(self, message: str) -> None:
        rgb("[*] " + str(message), (255, 0, 0))

    def __init__(self, *, verbose: bool = False):
        self.verbose    = verbose
        self.users      = []
        self.blockchain = []
        self._init_db()
        self._init_blockchain()

    #---------------------------------------------------------------
    
    
    def _init_blockchain(self) -> None:
        if os.path.isdir("data"):
            with open(self._blockchain_file, "r") as blockchain_file:
                self.blockchain = json.load(blockchain_file)["blocks"]
            self.log(f"loaded {len(self.blockchain)} blocks")

        else:
            genesis_block = { "index" : 0, "data" : "genocide", "proof" : 0, "prev_hash" : "0" * 64 }
            self.blockchain.append(genesis_block)
            with open(self._blockchain_file, "w") as blockchain_file:
                json.dump(
                        { "blocks" : self.blockchain },
                        blockchain_file,
                        indent=4
                    )

            self.log(f"created blockchain")

    def _create_block(self, data: list[dict], proof: int, prev_hash: str) -> dict:
        block = {
            "index" : len(self.blockchain),
            "data"  : data,
            "proof" : proof,
            "prev_hash" : prev_hash
        }
        return block

    def _proof_of_work(self, block: dict) -> int:
        """heavy operation"""
        new_proof = 1
        while True:
            block["proof"] = new_proof
            hash_value = self._block_hash(block)
            if hash_value[:self._difficulty] == "0" * self._difficulty:
                #print(hash_value) #DEBUG
                return new_proof
            else:
                new_proof += 1

    def _block_hash(self, block: dict) -> str:
        _ = json.dumps(block, sort_keys = True)
        return sha256(_.encode()).hexdigest()
    
    def _mine(self, data: list[dict]) -> None:
        prev_block = self.blockchain[-1]
        proof      = self._proof_of_work(prev_block)
        prev_hash  = self._block_hash(prev_block)
        block      = self._create_block(data, proof, prev_hash)
        self.blockchain.append(block) 
    
    #FIXME
    @property
    def is_blockchain_valid(self) -> bool:
        current_block = self.blockchain[0]
        block_index = 1
        
        while block_index < len(self.blockchain):
            next_block = self.blockchain[block_index]
            hash_value = self._block_hash(current_block)

            if next_block["prev_hash"] != hash_value:
                #TODO handle this
                self.error("previous hash does not match next hash")
                return False
            if hash_value[:self._difficulty] != "0" * self._difficulty: 
                #TODO HANDLE THIS
                self.error("hash is not valid")
                return False
            
            current_block = next_block
            block_index  += 1

        return True

    def _create_transaction(self, sender_id : int | str, receiver_id: int | str, amount : int ) -> dict:
        return { 
            "transaction_id" : len(self.blockchain),
            "timestamp"      : round(time.time()),
            "sender_id"      : sender_id,
            "receiver_id"    : receiver_id,
            "amount"         : round(amount)
        }

    def _add_transaction(self, sender_id : int | str, receiver_id: int | str, amount : int) -> None:
        transaction = self._create_transaction(sender_id, receiver_id, amount)
        self._mine(transaction)
        if type(sender_id) == str:
            self.log(f"#{len(self.blockchain)} {sender_id} -> {self[receiver_id]['name']} | {round(amount)}")
        else:
            self.log(f"#{len(self.blockchain)} {self[sender_id]['name']} -> {self[receiver_id]['name']} | {round(amount)}")
        self.warn("block mined!")

    #----------------------------------------------------------------

    def _init_db(self) -> None:
        if os.path.isdir("data"):
            # reading
            with open(self._users_file_name, 'r') as user_data_file:
                self.users = json.load( user_data_file )["users"]
            
            with open(self._blockchain_file, "r") as blockchain_file:
                self.blockchain = json.load( blockchain_file )["blocks"]
            
            self.log(f"loaded {len(self.users)} users")
        else:
            # create
            os.mkdir("data")
            self._save()
            self.log("database created")

    def _save(self) -> None:
        with open(self._users_file_name, "w") as data_file:
            json.dump(
                    { "users" : self.users },
                    data_file, 
                    indent=4
                )

        with open(self._blockchain_file, "w") as blockchain_file:
            json.dump(
                    { "blocks" : self.blockchain },
                    blockchain_file,
                    indent=4
                )

        self.log("database saved")

    def _money(self, id: int, amount: int) -> bool:
        tmp_user = self[id]
        if (tmp_user["amount"] + round(amount)) < 0: 
            return False
        tmp_user["amount"] += round(amount)
        self[id] = tmp_user
        return True

    #----------------------------------------------------------------

    def close(self) -> None:
        self._save()
        self.warn("closing database")

    def work(self, id: int) -> None:
        self._money(id, 25)
        self._add_transaction("bank", id, 25)

    def give(self, sender_id: int, receiver_id: int, amount: int) -> bool:
        if  self._money(sender_id, -amount):
            self._money(receiver_id, amount)
            self._add_transaction(sender_id, receiver_id, amount)
            return True
        else:
            return False

    def generate_csv(self) -> None:
        #TODO
        raise NotImplementedError

    def add_user(self, id: int, name: str) -> None:
        if id in self:
            return
        else:
            tmp_user = {
                "id"     : id,
                "name"   : name,
                "amount" : 0,
            }
            self.users.append(tmp_user)
            self.log(f"added {name} {id}")

    #----------------------------------------------------------------

    def __str__(self) -> str:
        return str([str(user) + "\n" for user in self.users])

    def __len__(self) -> int:
        return len(self.users)

    def __iter__(self):
        for user in self.users:
            yield user

    def __contains__(self, _id: int) -> bool:
        for user in self.users:
            if _id == user["id"]:
                return True
            else:
                continue
        else:
            return False

    def __getitem__(self, _id: int) -> dict:
        if _id in self:
            for user in self.users:
                if user["id"] == _id:
                    return user
        else:
            raise DatabaseException(f"Could not find user by id: {_id}")

    def __setitem__(self, _id: int, new_user: dict) -> None:
        if _id in self:
            for i in range(len(self.users)):
                if self.users[i]["id"] == _id:
                    self.users[i] = new_user
        else:
            # do this or insert new user, can be changed
            raise DatabaseException(f"Could not find user by id: {id}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_tb) -> None:
        if not exc_type == None:
            self.error(exc_type)
        if not exc_value == None:
            self.error(exc_value)
        if not exc_tb == None:
            self.error(exc_tb)
        self.close()

database = Database(verbose = True)

def test():
    _id = int(input("id > "))
    print("bal: ", database[_id]['amount'])
    while True:
        input("work...")
        database.work(_id)
        print("bal: ", database[_id]['amount'])
        print("valid", database.is_blockchain_valid)

if __name__ == '__main__':
    try:
        test()
    except KeyboardInterrupt:
        warn("keyboard interrupt")
    except Exception as e:
        warn(e)
    finally:
        database.close()