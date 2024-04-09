import hashlib
import json
from time import time
import uuid
from datetime import datetime
from typing import Any, Dict, Optional, List


class Block:
    def __init__(self, transaction: Optional[Dict[str, Any]], timestamp: float, previous_hash: str) -> None:
        """
        Initializes a new block.

        :param transaction: The data or transaction stored in the block.
        :param timestamp: The creation time of the block.
        :param previous_hash: The hash of the previous block in the chain.
        """
        self.id: str = str(uuid.uuid4())  # Unique identifier for the block
        self.transaction: Optional[Dict[str, Any]] = transaction  # Transaction data
        self.timestamp: float = timestamp  # Timestamp for when the block was created
        self.previous_hash: str = previous_hash  # Hash of the previous block in the chain
        self.hash: str = self.compute_hash()  # Current block's hash

    def compute_hash(self) -> str:
        """
        Computes the hash of the block.

        :return: The SHA-256 hash of the block's contents, excluding its own hash attribute.
        """
        block_string_dict = self.__dict__.copy()  # Copy of the block's data

        if 'hash' in block_string_dict:
            del block_string_dict['hash']  # Remove the hash field to avoid hashing the hash

        block_string = json.dumps(block_string_dict, sort_keys=True)  # Convert block to a sorted JSON string

        return hashlib.sha256(block_string.encode()).hexdigest()  # Return the SHA-256 hash of the string

    def __str__(self) -> str:
        """
        Provides a human-readable string representation of the block.

        :return: A string detailing the block's ID, timestamp, hash, and transaction data.
        """
        readable_time = datetime.utcfromtimestamp(self.timestamp).strftime('%Y-%m-%d %H:%M:%S.%f UTC')

        if self.transaction:
            transaction = json.dumps(self.transaction, indent=3)
        else:
            transaction = "Genesis Block"

        friendly_string = f"#{self.id} - {readable_time} - [{self.hash}]\n{transaction}"

        return friendly_string


class Blockchain:
    def __init__(self) -> None:
        """
        Initializes the blockchain with a genesis block.
        """
        self.chain: List[Block] = []
        self.create_genesis_block()

    def create_genesis_block(self) -> None:
        """
        Creates the first block in the blockchain (genesis block)
        """
        genesis_block = Block(None, time(), "0")
        self.chain.append(genesis_block)

    def add_block(self, transaction: Dict[str, Any]) -> None:
        """
        Adds a new block to the blockchain.

        :param transaction: The transaction data to be included in the new block.
        """
        previous_block = self.chain[-1]
        new_block = Block(transaction, time(), previous_block.hash)
        self.chain.append(new_block)

    def is_chain_valid(self) -> Dict[str, Any]:
        """
        Checks the integrity of the blockchain.

        :return: A dictionary indicating whether the blockchain is valid and detailing any issues found.
        """
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            if current.previous_hash != previous.hash:
                return {"Valid": False, "Issue": "Chain Link Failure", "Id": current.id}

            if current.hash != current.compute_hash():
                return {"Valid": False, "Issue": "Data Tampering", "Id": current.id}

        return {"Valid": True}

    def print_chain(self) -> None:
        """
        Prints a human-readable representation of the entire blockchain.
        """
        for block in self.chain:
            print(block)
