import os
import csv
import json
import time

from utils import *

class DatabaseException(Exception): pass

class Database:
    """
        super database v 1.0
        ~~~~~~~~~~~~~~~~~~~~~~~~~~

        
        \n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n
        \nstores: user dictionaries inside json
        
        \nGet started
        >>> database = Database()
        ... #or do
        >>> with Database(verbose=True) as db:
        ...   db.add_user(id, user_name)
        \n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n
        
        \nfeatures:

        \ndeposit:
        >>> if db.deposit(id, amount):
        >>>   success
        >>> else: fail, user has insufficient funds in their wallet

        \nwithdraw:
        >>> if db.withdraw(id, amount):
        >>>   success 
        >>> else: fail, user has insufficient funds in their bank

        \nmoney_bank
        >>> if db._bank(id, -100):
        >>>   success
        >>> else: fail, user has insufficient funds in their bank

        \nmoney_wallet
        >>> if db._wallet(id, -100):
        >>>   success
        >>> else: fail, user has insufficient funds in their wallet

        \n__contains__ implementation:
        >>> if user_id in db:
        >>> ...

        \n__getitem__ / __setitem__ implementation:
        >>> db[user_id]
        >>> db[user_id] = new_user

        \n__iter__ implementation:
        >>> for user in db:
        ...   print(user["id"])
        \n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n

        \nextras:
        >>> len(db) #get amount of users in db
        ... 101

        >>> str(db) #get every user dictionary in the db, all on new lines
        ... {"name": "John", "wallet": 6.9, "bank": 420.0}
        ... {"name": "Foo",  "wallet": 0.0, "bank": 200.0}
        ... ...
    """

    _file_name         = "data\\anarchist.json"
    _users_csv         = "data\\anarchist.csv"
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
        self.verbose      = verbose
        self.users        = []
        self.transactions = []
        self._init_db()


    #----------------------------------------------------------------


    def _add_transaction(self, sender_id: int, receiver_id: int, amount: int) -> None:
        self.transactions.append( { 
            "transaction_id" : len(self.transactions),
            "timestamp"      : round(time.time()),
            "sender_id"      : sender_id,
            "receiver_id"    : receiver_id,
            "amount"         : round(amount)
        } )
        self.warn(f"#{self.transactions[-1]['transaction_id']} {self[sender_id]['name']} -> {self[receiver_id]['name']} amount: {round(amount)}")

    def _init_db(self) -> None:
        if os.path.isfile(self._file_name):
            # reading
            with open(Database._file_name, 'r') as user_data_file, open(Database._transactions_file) as transactions_file:
                self.users        = json.load( user_data_file )["users"]
                self.transactions = json.load( transactions_file )["transactions"]
            
            self.log(f"loaded {len(self.users)} users | {len(self.transactions)} transactions")
        
        else:
            # create
            os.mkdir("data")
            self._save()
            self.log("database created")

    def _save(self) -> None:
        with open(Database._file_name, "w") as data_file:
            json.dump(
                    { "users" : self.users },
                    data_file, 
                    indent=4
                )

        with open(Database._transactions_file, "w") as transactions_file:
            json.dump(
                    { "transactions" : self.transactions },
                    transactions_file,
                    indent=4
                )

            self.log("database saved")

    def _money(self, id: int, amount: int) -> bool:
        tmp_user = self[id]
        if (tmp_user["amount"] + round(amount)) < 0: return False
        tmp_user["amount"] += round(amount)
        self[id] = tmp_user
        return True

    #----------------------------------------------------------------

    def close(self) -> None:
        """
            close the database, but this is a public method, and this is the one you 
            should use outside of the class.

            private methods *should* not be used outside of the class
            i said should, so you can still do db._save() without a problem
        """
        self._save()
        self.warn("closing database")

    def work(self, id: int) -> None:
        self._money(id, 25)
        self._add_transaction(id, id, 25)

    def give(self, sender_id: int, receiver_id: int, amount: int) -> bool:
        if  self._money(sender_id, -amount):
            self._money(receiver_id, amount)
            self._add_transaction(sender_id, receiver_id, amount)
            return True
        else:
            return False

    def generate_csv(self) -> None:
        """
            generate csv of the data.
            for our representation only, this is just so we can access the sheets
        """
        with open(Database._users_csv, "w", newline="", encoding="utf-8") as data_file:
            csv_writer = csv.writer(data_file)
            headers = False
            for user in self.users:
                if not headers:
                    csv_writer.writerow(user.keys())
                    headers = True
                csv_writer.writerow(user.values())

        with open(Database._transactions_csv, "w", newline="", encoding="utf-8") as data_file:
            csv_writer = csv.writer(data_file)
            headers = False

            csv_writer.writerow([
                "transaction_id",
                "sender_id",
                "sender_name",
                "receiver_id",
                "receiver_name",
                "amount"
            ])
            
            for transaction in self.transactions:
                csv_writer.writerow([
                            transaction["transaction_id"],
                            transaction["sender_id"],
                            self[transaction["sender_id"]]["name"],
                            transaction["receiver_id"],
                            self[transaction["receiver_id"]]["name"],
                            transaction["amount"]
                        ])
        
        self.warn("csv data sheets generated")

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