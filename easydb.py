import sqlite3

import json

from utils import *


def error(message: str) -> None:
    rgb("[!] " + str(message), (255, 0, 0))


def log(message: str) -> None:
    rgb("[*] " + str(message).replace("[*]", ""), 0x00ffff)


def warn(message: str) -> None:
    rgb("[-] " + str(message), (255, 255, 0))


class EasyDb:
    _difficulty = 4

    def __init__(self):
        self.connection = sqlite3.connect("data\\userdb.db")
        self.cursor     = self.connection.cursor()

    # ---------------------------------------------------------------

    def give(self, sender_id, receiver_id, amount):
        self.cursor.execute("""
        SELECT * FROM users
        WHERE id=?
        """, (sender_id, ))
        sender = list(self.cursor.fetchone())

        self.cursor.execute("""
        SELECT * FROM users
        WHERE id=?
        """, (receiver_id, ))
        receiver = list(self.cursor.fetchone())

        if sender[2] < amount:
            return False
        else:
            sender[2]   -= amount
            receiver[2] += amount
            self.cursor.execute("""
            UPDATE users 
            SET money=?
            WHERE id=?
            """, (sender[2], sender_id))

            self.cursor.execute("""
            UPDATE users 
            SET money=?
            WHERE id=? 
            """, (receiver[2], receiver_id))
            return True

    def get_user_money(self, _id: int) -> int:
        self.cursor.execute("""
        SELECT money FROM users
        WHERE id=?
        """, (_id,))
        return self.cursor.fetchone()

    def add_new_user(self, snowflake: int, username: str):
        self.cursor.execute("""
        INSERT INTO users(id, username) VALUES(?, ?);
        """, (snowflake, username))
        log(f"added {username} {snowflake}")

    def save(self):
        self.connection.commit()

    def close(self):
        self.connection.commit()
        self.connection.close()

    def _load_balances(self) -> None:
        self.cursor.execute("""
        UPDATE money
        SET money=0
        WHERE id<>924293465997705286
        """)

        # for block in self.blockchain:
        #     sender_id = block["data"]["sender_id"]
        #     receiver_id = block["data"]["receiver_id"]
        #     amount = block["data"]["amount"]
        #
        #     if not block["index"]:
        #         self["bank"].amount = amount
        #         continue
        #
        #     if not sender_id == "bank":
        #         self[sender_id] - amount
        #         self[receiver_id] + amount
        #     else:
        #         self[receiver_id] + amount
        #
        # self.log("balances overwritten")

    # ----------------------------------------------------------------
    def __contains__(self, _id: int) -> bool:
        self.cursor.execute("""
        SELECT username FROM users
        WHERE id=?
        """, (_id,))

        if self.cursor.fetchone():
            return True
        else:
            return False

    def __getitem__(self, _id: int) -> tuple:
        self.cursor.execute("""
        SELECT * FROM users
        WHERE id=?
        """, (_id,))
        return self.cursor.fetchone()

    def __enter__(self):
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            print(exc_type, exc_val, exc_tb, sep="\n")
            self.close()
        else:
            self.save()


database = EasyDb()


def migrate():
    with database as c:
        with open("data\\blockchain.json") as file:
            data = json.load(file)["blocks"]
            for b in data:
                c.execute("""
                INSERT INTO blocks
                VALUES(?,?,?,?,?,?,?)
                """, (
                        b["index"],
                        b["data"]["timestamp"],
                        b["data"]["sender_id"],
                        b["data"]["receiver_id"],
                        b["data"]["amount"],
                        b["proof"],
                        b["prev_hash"]
                    )
                )


if __name__ == '__main__':
    try:
        migrate()
    except KeyboardInterrupt:
        warn("keyboard interrupt")
    except Exception as e:
        warn(str(type(e)))
        warn(str(e))
    finally:
        database.close()

