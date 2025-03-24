import sys
sys.path.append(r'C:\Users\Shivam\Desktop\crypto-crafter')
import time
from Blockchain.Backend.core.block import Block
from Blockchain.Backend.core.blockheader import BlockHeader
from Blockchain.Backend.util.util import hash256
from Blockchain.Backend.core.database.database import BlockchainDB

ZERO_HASH = '0'*64
VERSION = 1

class Blockchain:
    def __init__(self):
        self.GenesisBlock()
    
    def write_on_disk(self, block):
        blockchainDB = BlockchainDB()
        blockchainDB.write(block)

    def fetch_last_block(self):
        blockchainDB = BlockchainDB()
        return blockchainDB.lastBlock()

    def GenesisBlock(self):
        BlockHeight = 0
        prevBlockHash = ZERO_HASH
        self.addBlock(BlockHeight, prevBlockHash)

    def addBlock(self, BlockHeight, prevBlockHash):
        timestamp = int(time.time())
        Transaction = f"Medusa Sent {BlockHeight} BTC to Shiviel"
        merkleRoot = hash256(Transaction.encode()).hex() # combined hash of all the transactions
        bits = "ffff001f"
        blockheader = BlockHeader(VERSION, prevBlockHash, merkleRoot, timestamp, bits)
        blockheader.mine()
        self.write_on_disk([Block(BlockHeight, 1, blockheader.__dict__, 1, Transaction).__dict__])

    def main(self):
        i = 0
        while i < 5:
            lastBlock = self.fetch_last_block()
            BlockHeight = lastBlock['Height'] + 1
            prevBlockHash = lastBlock['BlockHeader']['blockHash']
            self.addBlock(BlockHeight, prevBlockHash)
            i += 1

if __name__ == '__main__':
    blockchain = Blockchain()
    blockchain.main()