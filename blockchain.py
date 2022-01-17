import json
from hashlib import sha256
from supersecrets import digest

class BlockChain:
    _difficulty = 4
    _file_name  = "data\\blockchain.json"

    def __init__(self) -> None:
        self.chain = []
        self._create_genesis_block()

    def mine(self, data: dict) -> dict:
        prev_block = self.previous_block
        proof      = self._proof_of_work(prev_block)
        prev_hash  = self._hash(prev_block)
        block      = self._create_block(data, proof, prev_hash)
        self.chain.append(block)
        return block

    def _create_genesis_block(self) -> None:
        genesis_block = { "index" : 0, "data"  : "genocide", "proof" : 0, "previous_hash" : "0" * 64 }
        self.chain.append(genesis_block)

    def _create_block(self, data: dict, proof: int, prev_hash: str) -> dict:
        block = {
            "index" : len(self.chain),
            "data"  : data,
            "proof" : proof,
            "prev_hash" : prev_hash
        }
        return block
    
    def _proof_of_work(self, block: dict) -> int:
        """heavy operation"""
        new_proof = 1
        while True:
            block["proof"] = new_proof
            hash_value = self._hash(block)
            if hash_value[:self._difficulty] == "0" * self._difficulty:
                #print(hash_value) #DEBUG
                return new_proof
            else:
                new_proof += 1
    
    def _hash(self, block: dict) -> str:
        _ = json.dumps(block, sort_keys = True)
        return sha256(_.encode()).hexdigest()

    @property
    def previous_block(self):
        return self.chain[-1]

    @property
    def is_valid(self) -> bool:
        current_block = self.chain[0]
        block_index = current_block["index"]
        
        while block_index < len(self.chain):
            next_block = self.chain[block_index]
            if next_block["prev_hash"] != self._hash(current_block):
                return False

            current_proof = current_block["proof"]
            next_index = next_block["index"]
            next_data  = next_block["data"]
            next_proof = next_block["proof"]
            hash_value = digest(next_proof, current_proof, next_index, next_data)
            if hash_value[:4] != "0" * self._difficulty:
                return False
            
            current_block = next_block
            block_index  += 1

        return True


def main():
    t1 = {
        "transaction_id": 1,
        "sender_id"     : 725773984808960050,
        "receiver_id"   : 725773984808960050,
        "amount"        : 25
    }
    t2 = {
        "transaction_id": 2,
        "sender_id"     : 725773984808960050,
        "receiver_id"   : 725773984808960050,
        "amount"        : 100
    }

    bc = BlockChain()
    bc.mine(t1)
    bc.mine(t2)
    bc.mine(t2)
    bc.mine(t2)
    bc.mine(t2)
    print(bc.chain)

if __name__ == "__main__":
    main()