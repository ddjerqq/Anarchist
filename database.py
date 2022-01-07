import os
import csv
import json
import time

from utils import *

class DatabaseException(Exception):
    pass

class Database:
    """
        super database.           \n
        stores: User              \n
        >>> database = Database() \n
    """
    # data files
    __file_name = "data\\anarchist.json"
    __csv_name  = "data\\anarchist.csv"

    # utils
    def log(self, message: str) -> None:
        if self.verbose: rgb("[*] " + str(message).replace("[*]", ""), 0, 255, 255, newline=True)
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    #create the database
    def __init__(self, *, verbose: bool = False):
        #data
        self.verbose = verbose
        self.users   = []
        self._init_db()
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    #db private
    def _init_db(self) -> None:
        """
            initialize the database\n
            create if it doesn't exist, else read it.
        """
        if os.path.isfile(self.__file_name):
            # read
            with open(Database.__file_name, 'r') as data_file:
                self.users = json.load( data_file )["users"]
            self.log(f"loaded database with {len(self.users)} user") if len(self.users) == 1 else self.log(f"loaded database with {len(self.users)} users") #ensure it says 1 user 2 users.
        else:
            # create
            os.mkdir("data")
            with open(Database.__file_name, 'w') as data_file:
                json.dump( { "users" : self.users }, data_file, indent=4 )
            self.log(f"database created")

    def _save(self) -> None:
        """
            save the database.
        """
        with open(Database.__file_name, 'w') as data_file:
            json.dump( {"users" : self.users}, data_file, indent=4 )
            self.log("database saved")
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    #db public
    def close(self) -> None:
        self._save()
        self.log("closing database")

    def money_wallet(self, id: int, amount: float | str) -> int:
        """
            do stuff on wallet \n
            id: the id of the user
            amount: do "max" to get -all money\n
            returns: 1 on success, 0 on failure
        """
        tmp_user = self[id]

        if amount == "max":
            tmp_user["wallet"] -= tmp_user["wallet"]
            self[id] = tmp_user
            return 1
        else:
            if tmp_user["wallet"] + amount < -0.1:
                return 0
            else:
                tmp_user["wallet"] += amount
                self[id] = tmp_user
                return 1

    def money_bank(self, id: int, amount: float | str) -> int:
        """
            do stuff on bank \n
            id: the id of the user
            amount: do "max" to get -all money\n
            returns: 1 on success, 0 on failure
        """
        tmp_user = self[id]

        if amount == "max":
            tmp_user["bank"] -= tmp_user["bank"]
            self[id] = tmp_user
            return 1
        else:
            if tmp_user["bank"] + amount < -0.1:
                return 0
            else:
                tmp_user["bank"] += amount
                self[id] = tmp_user
                return 1

    def generate_csv(self) -> None:
        """
            generate csv of data.
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

    def add_user(self, id: int, name: str) -> int:
        """
            add a user object to database user dictionaries.\n
            saves automatically\n
            returns: int 0 on success 1 on user already in database
        """
        if id in self: return 1

        # create a user
        tmp_user = {
            "name"   : name,
            "id"     : id,
            "bank"   : 0.0,
            "wallet" : 0.0,
            "items"  : [],
        }
        self.users.append(tmp_user)
        self.log(f"added {name} {id}")
        # self._save()
        return 0
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    #dunder methods
    def __str__(self) -> str:
        return str([user for user in self.users])
    #in
    def __contains__(self, id: int) -> bool:
        for user in self.users:
            if id == user["id"]:
                return True
            else:
                continue
        else:
            return False
    #select the user by their id
    def __getitem__(self, id: int) -> dict:
        if id in self:
            for user in self.users:
                if user["id"] == id:
                    return user
        else:
            raise DatabaseException(f"Could not find user by id: {id}")
    #set user by id
    def __setitem__(self, id: int, new_user: dict) -> None:
        if id in self:
            for i in range( len(self.users) ):
                if  self.users[i]["id"] == id:
                    self.users[i] = new_user
        else:
            #do this or insert new user, can be changed
            raise DatabaseException(f"Could not find user by id: {id}")
    #get amount of users
    def __len__(self) -> int:
        return len(self.users)
    #context manager
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, exc_tb):
        if not exc_type == None:
            error(exc_type)
        if not exc_value == None:
            error(exc_value)
        if not exc_tb == None:
            error(exc_tb)
        self.close()
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~