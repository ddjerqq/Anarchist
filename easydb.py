import sqlite3
from datetime import datetime

from utils import *
from models.block import Block
from models.user import User


def error(message) -> None:
    rgb("[!] " + str(message), (255, 0, 0))


def log(message) -> None:
    rgb("[*] " + str(message).replace("[*]", ""), 0x00ffff)


def warn(message) -> None:
    rgb("[-] " + str(message), (255, 255, 0))


class EasyDb:
    _difficulty = 4
    _db_path = "C:\\work\\Python\\Anarchist\\data\\userdb.db"

    def __init__(self):
        self.connection = sqlite3.connect(self._db_path)
        self.cursor     = self.connection.cursor()
        self._load_balances()

    def get_user_money(self, _id: int) -> int:
        self.cursor.execute("""
        SELECT money FROM users
        WHERE id=?
        """, (_id,))
        return self.cursor.fetchone()

    def add_user(self, snowflake: int, username: str):
        self.cursor.execute("""
        INSERT INTO users(id, username)
        VALUES(?, ?);
        """, (snowflake, username))
        log(f"Added ({snowflake}) {username}")

    def give(self, sender_id, receiver_id, amount) -> bool:
        if self[sender_id].money >= amount:
            self._add_transaction(sender_id, receiver_id, amount)
            self.update()
            return True
        else:
            return False

    def update(self):
        self.connection.commit()

    def save(self):
        self.connection.commit()
        log("database saved")

    def close(self):
        self.connection.commit()
        self.connection.close()
        warn("database closed")

    def _load_balances(self) -> None:
        if not self.valid:
            raise Exception("invalid blockchain")

        # clear everyone's balances
        self.cursor.execute("""
        UPDATE users
        SET money=0
        """)
        log("balances cleared")

        # load users
        self.cursor.execute("""
        SELECT id, sender, recipient, amount 
        FROM blockchain
        """)
        blockchain = self.cursor.fetchall()

        for block in blockchain:
            index = block[0]
            sender_id = block[1]
            receiver_id = block[2]
            amount = block[3]

            if index == 0:
                self.cursor.execute("""
                UPDATE users
                SET money=money+?
                WHERE id=?;
                """, (amount, receiver_id))
                continue

            self.cursor.execute("""
            UPDATE users
            SET money=money-?
            WHERE id=?;
            """, (amount, sender_id))
            self.cursor.execute("""
            UPDATE users
            SET money=money+?
            WHERE id=?;
            """, (amount, receiver_id))
        self.update()

    def _add_block_to_db(self, block: Block) -> None:
        self.cursor.execute("""
        INSERT INTO blockchain(sender, recipient, amount, timestamp, proof, previous_hash, hash)
        VALUES(?, ?, ?, ?, ?, ?, ?);
        """, (
            block.sender_id,
            block.receiver_id,
            block.amount,
            block.timestamp,
            block.proof,
            block.previous_hash,
            block.hash
        ))

    def _create_block(self, sender_id: int, receiver_id: int, amount: int) -> Block:
        self.cursor.execute("""
        SELECT hash FROM blockchain
        WHERE id=(SELECT MAX(id) FROM blockchain);
        """)
        previous_hash = self.cursor.fetchone()[0]

        self.cursor.execute("""
        SELECT id FROM blockchain
        WHERE id=(SELECT MAX(id) FROM blockchain);
        """)
        index = self.cursor.fetchone()[0]

        return Block(
            index=index,
            sender_id=sender_id,
            receiver_id=receiver_id,
            amount=amount,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            previous_hash=previous_hash,
            proof=0
        )

    def _add_transaction(self, sender_id: int, receiver_id: int, amount: int) -> None:
        if not self.valid:
            return
        tmp_block = self._create_block(sender_id, receiver_id, amount)
        tmp_block.validate()
        self._add_block_to_db(tmp_block)

        self.cursor.execute("""
        UPDATE users
        SET money=money-?
        WHERE id=?;
        """, (amount, sender_id))

        self.cursor.execute("""
        UPDATE users
        SET money=money+?
        WHERE id=?;
        """, (amount, receiver_id))

        log(f"{self[sender_id].username} -> {self[receiver_id].username} {amount}")
        del tmp_block

    @property
    def valid(self) -> bool:
        # FIXME: this is not a valid blockchain
        # validate the blockchain
        self.cursor.execute("""
        SELECT previous_hash FROM blockchain
        WHERE id=(SELECT MAX(id) FROM blockchain);
        """)
        last_hash = self.cursor.fetchone()[0]

        self.cursor.execute("""
        SELECT hash FROM blockchain
        WHERE id=(SELECT MAX(id) FROM blockchain)-1;
        """)
        previous_hash = self.cursor.fetchone()[0]

        return last_hash == previous_hash

    def __contains__(self, value: int) -> bool:
        self.cursor.execute("""
        SELECT username FROM users
        WHERE id=?
        """, (value,))

        if self.cursor.fetchone():
            return True
        else:
            return False

    def __getitem__(self, value: int) -> User:
        self.cursor.execute("""
        SELECT * FROM users
        WHERE id=?
        """, (value,))
        return User.from_db(self.cursor.fetchone())

    def __enter__(self):
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            print(exc_type, exc_val, exc_tb, sep="\n")
            self.close()


database = EasyDb()


def test():
    pass


if __name__ == '__main__':
    try:
        test()
    except KeyboardInterrupt:
        warn("keyboard interrupt")
    except Exception as e:
        warn(str(type(e)))
        warn(str(e))
    finally:
        database.close()
