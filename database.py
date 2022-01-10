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
        >>> if db.money_bank(id, -100):
        >>>   success
        >>> else: fail, user has insufficient funds in their bank

        \nmoney_wallet
        >>> if db.money_wallet(id, -100):
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

    # static fields, this means the following data is a property of the Database class,
    # not a database object
    # to access these we do Database.__file_name not db.__file_name
    # because the file names will always be the same
    __file_name = "data\\anarchist.json"
    __csv_name = "data\\anarchist.csv"

    
    # utils

    def log(self, message: str) -> None:
        if self.verbose: rgb("[*] " + str(message).replace("[*]", ""), 0, 255, 255, newline=True)
    
    def error(self, message: str) -> None:
        if self.verbose: rgb("[*] " + str(message).replace("[*]", ""), 255, 0, 0, newline=True)
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    #create the database

    def __init__(self, *, verbose: bool = False):
        self.verbose = verbose
        self.users   = []
        self._init_db()

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    
    # properties
    # we dont have any properties yet, so just dont worry about this either.
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


    # private
    
    def _init_db(self) -> None:
        """
            initialize the database \n
            if the datafiles dont exist already:
                make them
            else:
                read them
        """
        if os.path.isfile(self.__file_name):
            # reading
            with open(Database.__file_name, 'r') as data_file:
                self.users = json.load( data_file )["users"]
            self.log(f"loaded database with {len(self.users)} user") if len(self.users) == 1 else self.log(f"loaded database with {len(self.users)} users") #ensure it says "1 user" "2 users".
        else:
            # create
            os.mkdir("data") # make the folder

            #this is a context manager lol
            with open(Database.__file_name, 'w') as data_file:
                json.dump( { "users" : self.users }, data_file, indent=4 )
            # we are saving {users : []}
            # so we can expand and possibly add more stuff to it idk
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
        with open(Database.__file_name, "w") as data_file:
            json.dump({"users": self.users}, data_file, indent=4)
            self.log("database saved")
  
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

    def money_wallet(self, id: int, amount: float) -> bool:
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
                >>> if db.money_wallet(id, -10):
                >>>   db.money_bank(id, 10)
                >>> else: # the user does not have enough money
        """

        tmp_user = self[id] # we get a temporary user dict

        if (tmp_user["wallet"] + amount) < -0.1:
            # if the amount is just a lil negative
            return False
        else:
            # if the amount is not negative, then we conduct the operation
            tmp_user["wallet"] += amount
            self[id] = tmp_user # __setitem__; self[id] = tmp_user is same as db[id] = tmp_user
            return True

    def money_bank(self, id: int, amount: float) -> int:
        """
            check docs for money_wallet, this is exactly the same, just on wallet
        """
        tmp_user = self[id]

        if tmp_user["bank"] + amount < -0.1:
            return 0
        else:
            tmp_user["bank"] += amount
            self[id] = tmp_user
            return 1

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
        if self.money_wallet(id, -amount):
            self.money_bank(id, amount)
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
        if self.money_bank(id, -amount):
            self.money_wallet(id, amount)
            return True
        else:
            return False

    def generate_csv(self) -> None:
        """
            generate csv of the data.
            for our representation only, this is just so we can access the sheets
        """
        with open(Database.__csv_name, "w", newline="", encoding="utf-8") as data_file:
            csv_writer = csv.writer(data_file)
            headers = False
            for user in self.users:
                if not headers:
                    header = user.keys()
                    csv_writer.writerow(header)
                    headers = True
                csv_writer.writerow(user.values())
            self.log("csv generated")

    def add_user(self, id: int, name: str) -> bool:
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
            return 1
        else:
            # create a temporary user
            tmp_user = {
                "id"     : id,
                "name"   : name,
                "bank"   : 0.0,
                "wallet" : 0.0,
                "items"  : [],
            }
            self.users.append(tmp_user)
            
            self.log(f"added {name} {id}")
            
            self._save()
            return False    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


    #dunder methods

    def __str__(self) -> str:
        """
            same as doing :
            >>> str(db)

            Args:
                None
            
            Returns:
                str: just gives you a string representation
        """
        return str([user + "\n" for user in self.users])

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
    
    def __len__(self) -> int:
        """
            >>> len(db)
            should be self explanatory and intuitive
        """
        return len(self.users)

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