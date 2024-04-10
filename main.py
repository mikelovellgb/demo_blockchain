import copy

from common.BlockChain import Blockchain

supply_chain = Blockchain()

supply_chain.add_block(transaction=
                       {
                           "action": "extract",
                           "asset_id": "1000",
                           "amount": "100kg",
                           "metal": "Gold",
                           "location": "Mine #45"
                       })

supply_chain.add_block(transaction=
                       {
                           "action": "extract",
                           "asset_id": "1001",
                           "amount": "150kg",
                           "metal": "Gold",
                           "location": "Mine #70"
                       })

supply_chain.add_block(transaction=
                       {
                           "action": "transfer",
                           "asset_id": "1000",
                           "amount": "100kg",
                           "metal": "Gold",
                           "location": "Mine A",
                           "destination": "Storage Facility #11"
                       })

supply_chain.add_block(transaction=
                       {
                           "action": "sell",
                           "asset_id": "1000",
                           "amount": "100kg",
                           "metal": "Gold",
                           "location": "Storage Facility #11",
                           "buyer": "91278"
                       })

# Valid at this point
supply_chain.print_chain()

print("Unmodified Blockchain")
print(f"Verify: {supply_chain.is_chain_valid()}")


# Take a copy to tamper with
tampered_chain = copy.deepcopy(supply_chain)

# Alter the transaction amount
print("Tampered, altering a transaction amount")
tampered_chain.chain[1].transaction["amount"] = "1000kg"

# Invalid at this point
print(f"Verify: {tampered_chain.is_chain_valid()}")


# Take a copy to tamper with
tampered_chain = copy.deepcopy(supply_chain)

# Alter the previous hash
print("Tampered, altering a previous hash on a record")
tampered_chain.chain[2].previous_hash = "abc123"

# Invalid at this point
print(f"Verify: {tampered_chain.is_chain_valid()}")

