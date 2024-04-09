import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from common.BlockChain import Block, Blockchain
from time import time


def test_block_creation():
    """Test that a Block is created with correct attributes."""
    transaction = {"sender": "Me", "you": "Bob", "amount": 10}
    timestamp = time()
    previous_hash = "abc123"
    block = Block(transaction, timestamp, previous_hash)

    assert block.transaction == transaction
    assert block.timestamp == timestamp
    assert block.previous_hash == previous_hash
    assert block.hash is not None  # Ensure a hash was generated


def test_compute_hash():
    """Test computing the hash of a block works correctly."""
    block = Block({"data": "test"}, time(), "0")
    expected_hash = block.compute_hash()
    assert block.hash == expected_hash


def test_block_str():
    """Test the string representation of a block."""
    block = Block({"data": "test"}, time(), "0")
    block_str = str(block)
    assert isinstance(block_str, str)
    assert block.id in block_str


def test_genesis_block_creation():
    """Test the genesis block is created correctly."""
    blockchain = Blockchain()
    assert len(blockchain.chain) == 1  # Only genesis block should be present


def test_add_block():
    """Test adding a block to the blockchain."""
    blockchain = Blockchain()
    transaction = {"sender": "Alice", "receiver": "Bob", "amount": 20}
    blockchain.add_block(transaction)
    assert len(blockchain.chain) == 2  # Now there should be two blocks

    # Check the transaction in the last block is correct
    added_block = blockchain.chain[-1]
    assert added_block.transaction == transaction


def test_is_chain_valid():
    """Test the blockchain's integrity validation."""
    blockchain = Blockchain()

    blockchain.add_block(transaction={"Something": "Good"})

    assert blockchain.is_chain_valid()["Valid"]  # Initially, the chain should be valid

    # Manually tampering with the chain to test validation
    blockchain.chain[1].transaction = {"tampered": True}
    assert not blockchain.is_chain_valid()["Valid"]


def test_print_chain(capsys):
    """Test that printing the chain does not cause errors and prints correctly."""
    blockchain = Blockchain()
    blockchain.print_chain()
    captured = capsys.readouterr()
    assert "Genesis Block" in captured.out
