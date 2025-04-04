import sys
sys.path.append(r'C:\Users\Shivam\Desktop\crypto-crafter')
import time
from Blockchain.Backend.core.block import Block
from Blockchain.Backend.core.blockheader import BlockHeader
from Blockchain.Backend.util.util import hash256, merkle_root, target_to_bits
from Blockchain.Backend.core.database.database import BlockchainDB
from Blockchain.Backend.core.Tx import CoinbaseTx
from multiprocessing import Process, Manager
from Blockchain.Frontend.run import main

ZERO_HASH = '0'*64
VERSION = 1
INITIAL_TARGET = 0x0000ffff00000000000000000000000000000000000000000000000000000000

class Blockchain:
    def __init__(self, utxos, MemPool):
        """
        Initialize Blockchain instance
        :param utxos: A dict of all the unspent transaction
        """
        self.utxos = utxos
        self.MemPool = MemPool
        self.current_target = INITIAL_TARGET
        self.bits = target_to_bits(INITIAL_TARGET)
    
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

    def store_utxos_in_cache(self):
        """Keep track of all the unspent transaction in cache memory for fast retieval"""
        for tx in self.addTransactionsInBlock:
            print(f"Transaction added {tx.TxId}")
            self.utxos[tx.TxId] = tx
        
    def remove_spent_Transactions(self):
        for txId_index in self.remove_spent_transactions:
            if txId_index[0].hex() in self.utxos:
                if len(self.utxos[txId_index[0].hex()].tx_outs) < 2:
                    del self.utxos[txId_index[0].hex()]
                    print(f"Spent Transaction removed {txId_index[0].hex()}")
                else:
                    prev_trans = self.utxos[txId_index[0].hex()]
                    self.utxos[txId_index[0].hex()] = prev_trans.tx_outs.pop(txId_index[1])

    def remove_transactions_from_memorypool(self):
        """Remove Transactions from Memory Pool"""
        for tx in self.TxIds:
            if tx.hex() in self.MemPool:
                del self.MemPool[tx.hex()]
                print(f"Transaction removed from Memory Pool {tx.hex()}")

    def read_transaction_from_memorypool(self):
        """Read Transactions from Memory Pool"""
        self.Blocksize = 80
        self.TxIds = []
        self.addTransactionsInBlock = []
        self.remove_spent_transactions = []

        for tx in self.MemPool:
            self.TxIds.append(bytes.fromhex(tx))
            self.addTransactionsInBlock.append(self.MemPool[tx])
            self.Blocksize += len(self.MemPool[tx].serialize())

            for spent in self.MemPool[tx].tx_ins:
                self.remove_spent_transactions.append([spent.prev_tx, spent.prev_index])

    def convert_to_json(self):
        self.TxJson = []

        for tx in self.addTransactionsInBlock:
            self.TxJson.append(tx.to_dict())

    def calculate_fee(self):
        self.input_amount = 0
        self.output_amount = 0

        """Calculate input amount"""
        for TxId_index in self.remove_spent_transactions:
            if TxId_index[0].hex() in self.utxos:
                self.input_amount += self.utxos[TxId_index[0].hex()].tx_outs[TxId_index[1]].amount

        """Calculate output amount"""
        for tx in self.addTransactionsInBlock:
            for tx_out in tx.tx_outs:
                self.output_amount += tx_out.amount
        
        self.fee = self.input_amount - self.output_amount

    def addBlock(self, BlockHeight, prevBlockHash):
        self.read_transaction_from_memorypool()
        self.calculate_fee()
        timestamp = int(time.time())
        # Transaction = f"Medusa Sent {BlockHeight} BTC to Shiviel"
        coinbaseInstance = CoinbaseTx(BlockHeight)
        coinbaseTx = coinbaseInstance.CoinbaseTransaction()
        self.Blocksize += len(coinbaseTx.serialize())

        coinbaseTx.tx_outs[0].amount = coinbaseTx.tx_outs[0].amount + self.fee

        self.TxIds.insert(0, bytes.fromhex(coinbaseTx.id()))
        self.addTransactionsInBlock.insert(0, coinbaseTx)

        merkleRoot = merkle_root(self.TxIds)[::-1].hex()
        blockheader = BlockHeader(VERSION, prevBlockHash, merkleRoot, timestamp, self.bits)
        blockheader.mine(self.current_target)

        self.remove_spent_Transactions()
        self.remove_transactions_from_memorypool()
        self.store_utxos_in_cache()
        self.convert_to_json()

        print(f"Block {BlockHeight} Mined Successfully with Nonce value of {blockheader.nonce}")
        self.write_on_disk([Block(BlockHeight, self.Blocksize, blockheader.__dict__, 1, self.TxJson).__dict__])

    def main(self):
        i = 0
        lastBlock = self.fetch_last_block()
        if lastBlock is None:
            self.GenesisBlock()
            
        while True:
            lastBlock = self.fetch_last_block()
            BlockHeight = lastBlock['Height'] + 1
            prevBlockHash = lastBlock['BlockHeader']['blockHash']
            self.addBlock(BlockHeight, prevBlockHash)

if __name__ == '__main__':
    with Manager() as manager:
        utxos = manager.dict()
        MemPool = manager.dict()

        webapp = Process(target=main, args=(utxos, MemPool))
        webapp.start()

        blockchain = Blockchain(utxos, MemPool)
        blockchain.main()