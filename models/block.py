from hashlib import sha256
from supersecrets import SECRET


class Block(object):
    _difficulty = 4

    def __init__(
            self,
            index: int,
            timestamp: str,
            sender_id: int,
            receiver_id: int,
            amount: int,
            proof: int,
            previous_hash: str) -> None:
        """
        Initialize a Block object
        :param index: int
        :param timestamp: int
        :param sender_id: int
        :param receiver_id: int
        :param amount: int
        :param proof: int
        :param previous_hash: str(64)
        """
        self.index = index
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.amount = amount
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.proof = proof

    # THIS IS HEAVY OPERATION
    def validate(self) -> None:
        while not self.valid:
            self.proof += 1

    @property
    def hash(self):
        a  = str((self.index + self.sender_id + self.receiver_id + self.amount) * (self.proof + 1)) + self.previous_hash
        a += SECRET
        return sha256(a.encode()).hexdigest()

    @property
    def valid(self) -> bool:
        return self.hash[0:self._difficulty] == "0" * self._difficulty

    @property
    def to_db(self) -> tuple:
        return (
            self.sender_id,
            self.receiver_id,
            self.amount,
            self.timestamp,
            self.proof,
            self.previous_hash,
            self.hash)

    @staticmethod
    def from_db(block_tuple) -> "Block":
        return Block(
            block_tuple[0],
            block_tuple[4],
            block_tuple[1],
            block_tuple[2],
            block_tuple[3],
            block_tuple[5],
            block_tuple[6])

    @staticmethod
    def from_index(index: int, db) -> "Block":
        with db as c:
            c.execute("""
            SELECT * FROM blockchain
            WHERE id=?
            """, (index,))
            data = c.fetchone()
            if data:
                return Block(
                    data[0],
                    data[1],
                    data[2],
                    data[3],
                    data[4],
                    data[5],
                    data[6])
            else:
                c.execute("""
                SELECT * FROM blockchain
                WHERE id=(SELECT MAX(id) FROM blockchain)
                """)
                block = Block.from_db(c.fetchone())
                return block

    @staticmethod
    def last_block(db) -> "Block":
        with db as c:
            c.execute("""
            SELECT * FROM blockchain
            WHERE id=(SELECT MAX(id) FROM blockchain)
            """)
            return Block.from_db(c.fetchone())

    def __str__(self) -> str:
        return f"{self.index} {self.sender_id} {self.receiver_id} {self.amount}" + \
               f"{self.timestamp} {self.proof} {self.previous_hash} {self.hash}"

    def __del__(self) -> None:
        del self.index
        del self.sender_id
        del self.receiver_id
        del self.amount
        del self.timestamp
        del self.previous_hash
        del self.proof
