import os
import csv
import json
import time
from datetime import datetime

from hashlib import sha256
from models.user import User

from utils import *

class DatabaseException(Exception): 
    pass

class Database:
    _difficulty        = 4
    _blockchain_file   = "data\\blockchain.json"

    _users_file_name   = "data\\anarchist.json"
    _transactions_file = "data\\transactions.json"

    _blockchain_csv    = "data\\blockchain.csv"
    _users_csv         = "data\\blockchain.csv"

    def log(self, message: str) -> None:
        if self.verbose:
            rgb("[*] " + str(message).replace("[*]", ""), 0x00ffff)

    def warn(self, message: str) -> None:
        if self.verbose:
            rgb("[*] " + str(message), (255, 255, 0))

    def error(self, message: str) -> None:
        rgb("[*] " + str(message), (255, 0, 0))

    def __init__(self, *, verbose: bool = False):
        self.verbose    = verbose
        self.users     : list[User] = []
        self.blockchain: list[dict] = []
        self._init_db()
        self._load_balances()

    #---------------------------------------------------------------
    
    def close(self) -> None:
        self._save()
        self.generate_csv()
        self.warn("closing database")

    def give(self, sender_id: int, receiver_id: int, amount: int) -> bool:
        """
        same as work
        >>> give(bank, user, 50)
        true on success
        false on fail
        """
        if  sender_id == "bank":
            self[receiver_id] + amount
            self._add_transaction(sender_id, receiver_id, amount)
            return True
        if round(amount) < self[sender_id].amount:
            self[receiver_id] + amount
            self[sender_id]   - amount
            self._add_transaction(sender_id, receiver_id, amount)
            return True
        else:
            return False

    def generate_csv(self) -> None:
        with open(self._blockchain_csv, "w", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)

            writer.writerow(
                ["index", "time", "sender", "receiver", "amount"]
                )

            for block in self.blockchain:
                writer.writerow([
                    block["index"],
                    str(datetime.fromtimestamp(block["data"]["timestamp"])),
                    self[block["data"]["sender_id"]].name,
                    self[block["data"]["receiver_id"]].name,
                    block["data"]["amount"]
                ])

    def add_user(self, _id: int, name: str) -> None:
        if _id in self:
            raise DatabaseException(f"user {_id} already in database")
        else:
            tmp_user = User(_id, name)
            self.users.append(tmp_user)
            self.log(f"added {tmp_user}")

    def _load_balances(self) -> None:
        if not self.is_blockchain_valid: 
            raise DatabaseException("blockchain is not valid")

        #reset users
        for user in self.users:
            if user.name != "bank":
                user.amount = 0

        for block in self.blockchain:
            sender_id   = block["data"]["sender_id"]
            receiver_id = block["data"]["receiver_id"]
            amount      = block["data"]["amount"]
            
            if not block["index"]: 
                self["bank"].amount = amount
                continue

            if not sender_id == "bank":
                self[sender_id]   - amount
                self[receiver_id] + amount
            else:
                self[receiver_id] + amount
        
        self.log("balances overwritten")

    @property
    def is_blockchain_valid(self) -> bool:
        current_block = self.blockchain[0]
        block_index = 1
        
        while block_index < len(self.blockchain):
            next_block = self.blockchain[block_index]
            cur_hash_value = self._block_hash(current_block)

            
            if next_block["prev_hash"] != cur_hash_value:
                #TODO handle this
                print(next_block["prev_hash"])
                print(cur_hash_value)
                self.error("previous hash does not match next hash")
                return False
            if cur_hash_value[:self._difficulty] != "0" * self._difficulty: 
                #TODO HANDLE THIS
                print(cur_hash_value)
                self.error("hash is not valid")
                return False
            
            current_block = next_block
            block_index  += 1

        return True

    def _create_block(self, data: list[dict], proof: int, prev_hash: str) -> dict:
        block = {
            "index" : len(self.blockchain),
            "data"  : data,
            "proof" : proof,
            "prev_hash" : prev_hash
        }
        return block

    def _find_proof(self, block: dict) -> int:
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
        return sha256(json.dumps(block).encode()).hexdigest()
    
    def _mine(self, data: list[dict]) -> None:
        prev_block = self.blockchain[-1]
        proof      = self._find_proof(prev_block)
        prev_hash  = self._block_hash(prev_block)
        block      = self._create_block(data, proof, prev_hash)
        self.blockchain.append(block) 
    
    def _add_transaction(self, sender_id : int | str, receiver_id: int | str, amount : int) -> None:
        if not self.is_blockchain_valid:
            raise DatabaseException("blockchain is not valid")
        transaction = {
            "timestamp"   : round(time.time()),
            "sender_id"   : sender_id,
            "receiver_id" : receiver_id,
            "amount"      : round(amount)
            }
        self._mine(transaction)

        self.log(f"#{len(self.blockchain)} {self[sender_id].name} -> {self[receiver_id].name} : {round(amount)}")

    def _init_db(self) -> None:
        with open(self._users_file_name, 'r') as user_data_file:
            for user_dict in json.load( user_data_file )["users"]:
                self.users.append( User.from_dict(user_dict) )

        with open(self._blockchain_file, "r") as blockchain_file:
            self.blockchain = json.load( blockchain_file )["blocks"]

        self.log(f"loaded {len(self.users)} users")

    def _save(self) -> None:
        with open(self._users_file_name, "w") as data_file:
            json.dump(
                    { "users" : [user.dict for user in self.users] },
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

    #----------------------------------------------------------------
    def __contains__(self, _id: int) -> bool:
        for user in self.users:
            if _id == user.id:
                return True
            else:
                continue
        else:
            return False

    def __getitem__(self, _id: int) -> User:
        if _id in self:
            for user in self.users:
                if user.id == _id:
                    return user
        else:
            raise KeyError(f"Could not find user by id: {_id}")

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
    database._load_balances()
    database.give("bank", 725773984808960050, 1750)

if __name__ == '__main__':
    try:
        test()
    except KeyboardInterrupt:
        warn("keyboard interrupt")
    except Exception as e:
        warn(e)
    finally:
        database.close()