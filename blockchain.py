import json
import time
from hashlib import sha256


class BlockChain:
    _difficulty = 5

    def __init__(self):
        self.chain = []
        self.add_block(0, "initial", "")

    def add_block(self, proof, previous_hash, transaction_data) -> dict:
        block = {
            "index": len(self.chain),
            "proof": proof,
            "previous_hash": previous_hash,
            "transactions": transaction_data,
        }
        self.chain.append(block)
        return block

    # This function is created
    # to display the previous block
    @property
    def last_block(self) -> dict:
        return self.chain[-1]

    # This is the function for proof of work
    # and used to successfully mine the block
    def proof_of_work(self, previous_proof) -> int:
        new_proof = 1
        check_proof = False

        while check_proof is False:
            hash_operation = sha256(
                str(new_proof ** 2 - previous_proof ** 2).encode()
            ).hexdigest()

            if hash_operation[: BlockChain._difficulty] == "0" * BlockChain._difficulty:
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def hash_block(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return sha256(encoded_block).hexdigest()

    def chain_valid(self):
        previous_block = self.chain[0]
        for block_index in range(1, len(self.chain)):
            block = self.chain[block_index]
            if block["previous_hash"] != self.hash_block(previous_block):
                return False

            previous_proof = previous_block["proof"]
            proof = block["proof"]
            hash_operation = sha256(
                str(proof ** 2 - previous_proof ** 2).encode()
            ).hexdigest()

            if hash_operation[: BlockChain._difficulty] != "0" * BlockChain._difficulty:
                return False
            previous_block = block

        return True

    def mine(self):
        proof = self.proof_of_work(self.last_block["proof"])
        previous_hash = self.hash_block(self.last_block)
        block = self.add_block(proof, previous_hash, "sender_id-receiver_id:amount;")

        print()
        print("new block is mined!")
        print("index:", block["index"])
        print("proof:", block["proof"])
        print("data:", block["transactions"])
        print("hash:", self.hash_block(block))
        print("prev:", block["previous_hash"])


blockchain = BlockChain()
blockchain.mine()
blockchain.mine()
blockchain.mine()
blockchain.mine()

print()
for block in blockchain.chain:
    print(block)

print()
print(blockchain.chain_valid())
