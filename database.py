import os
import csv
import json
import time

from utils import *

class DatabaseException(Exception):
    pass

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

    _file_name        = "data\\anarchist.json"
    _users_csv        = "data\\anarchist.csv"
    _transactions_csv = "data\\transactions.csv"

    # static methods

    # utils

    def log(self, message: str) -> None:
        if self.verbose:
            rgb("[*] " + str(message).replace("[*]", ""), (0, 255, 255))

    def error(self, message: str) -> None:
        if self.verbose:
            rgb("[*] " + str(message).replace("[*]", ""), (255, 0, 0))

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # create the database

    def __init__(self, *, verbose: bool = False):
        self.verbose      = verbose
        self.users        = []
        self.transactions = []
        self._init_db()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # properties
    # we dont have any properties yet, so just dont worry about this either.
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # private
    def _add_transaction(self, sender_id: int | str, receiver_id: int | str, /, wallet: float = 0, bank: float = 0) -> None:
        """
            add transaction to the database
            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

            Args:
                sender   (int | str): sender id or service name
                receiver (int | str): receiver id or service name
                wallet   (float): amount to be added to the wallet
                bank     (float): amount to be added to the bank
            
            Returns:
                None
        """
        self.transactions.append( { 
            "transaction_id" : len(self.transactions),
            "sender_id"      : sender_id,
            "sender_name"    : self[sender_id]["name"],
            "receiver_id"    : receiver_id,
            "receiver_name"  : self[receiver_id]["name"],
            "wallet"         : wallet,
            "bank"           : bank
        } )
        self.log(f"#{self.transactions[-1]['transaction_id']} {self[sender_id]['name']} -> {self[receiver_id]['name']} wallet: {wallet} bank: {bank}")

    def _init_db(self) -> None:
        """
        initialize the database \n
        if the datafiles dont exist already:
            make them
        else:
            read them
        """
        if os.path.isfile(self._file_name):
            # reading
            with open(Database._file_name, 'r') as data_file:
                data = json.load( data_file )
                self.users        = data["users"]
                self.transactions = data["transactions"]
            self.log(f"loaded database with {len(self.users)} users and {len(self.transactions)} transactions")
        
        else:
            # create
            os.mkdir("data")  # make the folder

            #this is a context manager lol
            with open(Database._file_name, 'w') as data_file:
                json.dump( 
                        { 
                            "users"        : self.users, 
                            "transactions" : self.transactions 
                        }, 
                        data_file, 
                        indent=4 
                    )
            
            self.log(f"database created")

    def _save(self) -> None:
        """
        save the database.
        from memory to disk,
        we are dumping self.users to datafile.json inside the \n
        {
            users : self.users
        }
        """
        with open(Database._file_name, "w") as data_file:
            json.dump(
                    {
                        "users"        : self.users,
                        "transactions" : self.transactions 
                    },
                    data_file, 
                    indent=4
                )
            self.log("database saved")

    def _wallet(self, id: int, amount: float) -> bool:
        """
        add or subtract amount from the wallet
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        Args:
            id (int): the id of the user
            amount (float): keep in mind you can pass -10 as an argument.

        Returns:
            True on success, False on failure,
            this could fail if the user has insufficient funds

            Example:
                >>> if db._wallet(id, -10):
                >>>   db._bank(id, 10)
                >>> else: # the user does not have enough money
        """

        tmp_user = self[id]  # we get a temporary user dict

        if (tmp_user["wallet"] + amount) < -0.1:
            # if the amount is just a lil negative
            return False
        else:
            # if the amount is not negative, then we conduct the operation
            tmp_user["wallet"] += amount
            self[id] = tmp_user
            return True

    def _bank(self, id: int, amount: float) -> int:
        """
            check docs for _wallet, this is exactly the same, just on wallet
        """
        tmp_user = self[id]

        if tmp_user["bank"] + amount < -0.1:
            return 0
        else:
            tmp_user["bank"] += amount
            self[id] = tmp_user
            return 1

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # public
    def close(self) -> None:
        """
            close the database, but this is a public method, and this is the one you 
            should use outside of the class.

            private methods *should* not be used outside of the class
            i said should, so you can still do db._save() without a problem
        """
        self._save()
        self.log("closing database")

    def work(self, id: int) -> None:
        """
            work command\n
            tracked transaction
        """
        self._wallet(id, 25)
        self._add_transaction("work", id, 25, 0)

    def deposit(self, id: int, amount: float) -> bool:
        """
        an easier way to deposit funds from an users wallet to their bank.

        Args:
            id (int): id of the user
            amount (float): amount to deposit

        Returns:
            True on success
            False on fail (if user has insufficient funds)

        Example:
            >>> if db.deposit(id, 10):
            >>>   user deposit success
            >>> else: user has insufficient funds
        """
        if self._wallet(id, -amount):
            self._bank(id, amount)
            self._add_transaction(id, id, amount, -amount)
            return True
        else:
            return False

    def withdraw(self, id: int, amount: float) -> bool:
        """
            an easier way to withdraw funds from an users bank to their wallet.

            Args:
                id (int): id of the user
                amount (float): amount to deposit

            Returns:
                True on success
                False on fail (if user has insufficient funds)

            Example:
                >>> if db.withdraw(id, 10):
                >>>   user withdraw success
                >>> else: user has insufficient funds
        """
        if self._bank(id, -amount):
            self._wallet(id, amount)
            self._add_transaction(id, id, amount, -amount)
            return True
        else:
            return False

    def give(self, sender_id: int, receiver_id: int, amount: float) -> bool:
        """
            take money from one user's wallet to another
            tracked transaction

            Args:
                sender_id (int)  : The sender's id
                receiver_id (int): The receiver's id
                amount (float)   : The amount to give

            Returns:
                bool: True on success, False on fail
            
            Example:
                >>> if database.give(ctx.author.id, _id, amount):
                >>>   success
                >>> else: fail
        """
        if self._wallet(sender_id, -amount):
            self._wallet(receiver_id, amount)
            self._add_transaction(sender_id, receiver_id, wallet = amount)
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
            for transaction in self.transactions:
                if not headers:
                    csv_writer.writerow(transaction.keys())
                    headers = True
                csv_writer.writerow(transaction.values())
        
        self.log("csv data sheets generated")

    def add_user(self, id: int, name: str) -> None:
        """
            add a user dict to database user dictionaries.
            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            (saves automatically)

            Args:
                id (int): the id of the user
                name (str): the name of the user

            Returns:
                bool: True if the user was already in the database, False otherwise
        """

        if id in self:
            return
        else:
            # create a temporary user
            tmp_user = {
                "id": id,
                "name": name,
                "bank": 0.0,
                "wallet": 0.0,
            }

            self.users.append(tmp_user)

            self.log(f"added {name} {id}")

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # dunder methods

    def __str__(self) -> str:
        """
            same as doing :
            >>> str(db)

            Args:
                None

            Returns:
                str: just gives you a string representation
        """
        return str([str(user) + "\n" for user in self.users])

    def __iter__(self):
        """
            >>> for user in db
            >>>   print(user)

            this is used when we iterate over the databse,
            and yes this is very useless, we can just do

            >>> for user in db.users:
            >>>   print(user)

            both ways work perfectly fine and we dont need to worry about it much
        """
        for user in self.users:
            yield user

    def __contains__(self, id: int) -> bool:
        """
            >>> user_id in database

            Args:
                None

            Returns:
                bool: True if id is in the database, False otherwise
        """
        for user in self.users:
            if id == user["id"]:
                return True
            else:
                continue
        else:
            return False

    def __getitem__(self, id: int) -> dict:
        """
            get whole user dictionary from the database by just doing
            >>> db[id]

            Args:
                id (int): id of the user

            Retruns:
                dict: dictionary of the user with that id

            Raises:
                DatabaseException: if the user does not exist in the database
        """
        if id in self:
            for user in self.users:
                if user["id"] == id:
                    return user
        else:
            raise DatabaseException(f"Could not find user by id: {id}")

    def __setitem__(self, id: int, new_user: dict) -> None:
        """
            same as __getitem__ but this time, we are setting the item in the database, not just reading

            >>> new_user = {"name": "something"}
            >>> db[id] = new_user

            Args:
                new_user (dict): the user which you are assigning to the id

            Returns:
                None

            Raises:
                DatabaseException: when user not found
        """
        if id in self:
            for i in range(len(self.users)):
                if self.users[i]["id"] == id:
                    self.users[i] = new_user
        else:
            # do this or insert new user, can be changed
            raise DatabaseException(f"Could not find user by id: {id}")

    def __enter__(self):
        """
            context managers, very useful stuff if you wanna quickly do stuff on the db
            this is called when you do
            >>> with database as db:
            >>>   db.add_user(id)

            Returns:
                self, the database basically

            __enter__ by itself has no meaning, it is useless, unless we implement 🔽
        """
        return self

    def __exit__(self, exc_type, exc_value, exc_tb) -> None:
        """
            this is called when we are done operating on the database using the context manager
            if any error happens, we print that with red color

            Args:
                exc_type: exception type
                exc_value: exception value
                exc_tb: exception traceback
                # we are not really handling those exceptions because we dont need to so its ok

            Returns: None
        """
        if not exc_type == None:
            self.error(exc_type)
        if not exc_value == None:
            self.error(exc_value)
        if not exc_tb == None:
            self.error(exc_tb)
        self.close()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~