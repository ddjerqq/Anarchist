import time
from hashlib import sha256
from supersecrets import digest

class BlockChain:
    _difficulty = 4
    _file_name  = "data\\blockchain.json"
    _csv_name   = "data\\blockchain.csv"

    def __init__(self) -> None:
        self.chain    = []
        genesis_block = self._create_block(0, {"genesis block" : "super"}, 0, "0")
        self.chain.append(genesis_block)

    def mine_block(self, data: dict) -> dict:
        if not self.chain_valid:
            raise Exception("the blockchain is invalid")
        block = self._mine_block(data)
        return block

    @property
    def previous_block(self) -> dict:
        return self.chain[-1]

    @property
    def chain_valid(self) -> bool:
        current_block = self.chain[0]
        block_index   = 1

        while block_index < len(self.chain):
            next_block = self.chain[block_index]
            if next_block["previous_hash"] != self._hash(current_block):
                return False

            current_proof = current_block["proof"]
            next_index = next_block["index"]
            next_data  = next_block["data"]
            next_proof = next_block["proof"]

            hash_value = sha256(
                self._to_digest(next_proof, current_proof, next_index, next_data)
            ).hexdigest()

            if hash_value[:self._difficulty] != "0" * self._difficulty:
                return False
            
            current_block = next_block
            block_index += 1

        return True

    def _mine_block(self, data: dict) -> dict:
        previous_block = self.previous_block
        previous_proof = previous_block["proof"]
        index = previous_block["index"] + 1
        proof = self._proof_of_work(previous_proof, index, data)
        previous_hash = self._hash(previous_block)
        block = self._create_block(index, data, proof, previous_hash)
        self.chain.append(block)
        return block

    def _hash(self, block: dict) -> str:
        """
            hash a block and return the cryptographic hash
        """
        return sha256(str(block).encode()).hexdigest()

    def _proof_of_work(self, previous_proof: int, index: int, data: dict) -> int:
        """
            heavy operation
        """
        new_proof = 1
        while True:
            to_digest = digest(new_proof, previous_proof, index, data)
            hash_value = sha256(to_digest).hexdigest()
            if hash_value[:self._difficulty] == "0" * self._difficulty:
                return new_proof
            else:
                new_proof += 1

    def _create_block(self,
            index         : int,
            data          : dict,
            proof         : int,
            previous_hash : str )  -> dict:
        block = {
            "index"         : index,
            "data"          : data,
            "proof"         : proof,
            "previous_hash" : previous_hash
        }

        return block


t1 = {
    "transaction_id": 0,
    "sender_id"     : 725773984808960050,
    "receiver_id"   : 725773984808960050,
    "amount"        : 25
}
t2 = {
    "transaction_id": 1,
    "sender_id"     : 725773984808960050,
    "receiver_id"   : 725773984808960050,
    "amount"        : 25
}
t3 = {
    "transaction_id": 2,
    "sender_id"     : 725773984808960050,
    "receiver_id"   : 923600698967461898,
    "amount"        : 10
}