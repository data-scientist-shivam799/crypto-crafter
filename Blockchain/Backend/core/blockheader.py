from Blockchain.Backend.util.util import hash256

class BlockHeader:
    def __init__(self, version, prevBlockHash, merkleRoot, timestamp, bits):
        self.version = version
        self.prevBlockHash = prevBlockHash
        self.merkleRoot = merkleRoot
        self.timestamp = timestamp
        self.bits = bits
        self.nonce = 0
        self.blockHash = ''

    def mine(self):
        while (self.blockHash[0:4] != '0000'):
            self.blockHash = hash256((str(self.version) + self.prevBlockHash + self.merkleRoot + 
                                     str(self.timestamp) + self.bits + str(self.nonce)).encode()).hex()
            self.nonce += 1
            print(f"Mining started {self.nonce}", end='\r')
