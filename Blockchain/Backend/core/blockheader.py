from Blockchain.Backend.util.util import hash256, little_endian_to_int, int_to_little_endian

class BlockHeader:
    def __init__(self, version, prevBlockHash, merkleRoot, timestamp, bits):
        self.version = version
        self.prevBlockHash = prevBlockHash
        self.merkleRoot = merkleRoot
        self.timestamp = timestamp
        self.bits = bits
        self.nonce = 0
        self.blockHash = ''

    def mine(self, target):
        self.blockHash = target + 1

        while self.blockHash > target:
            self.blockHash = little_endian_to_int(hash256(int_to_little_endian(self.version, 4) + bytes.fromhex(self.prevBlockHash)[::-1] +
                                                          bytes.fromhex(self.merkleRoot) + int_to_little_endian(self.timestamp, 4) +
                                                          self.bits + int_to_little_endian(self.nonce, 4)))
            self.nonce += 1
            print(f"Mining started {self.nonce}", end='\r')

        self.blockHash = int_to_little_endian(self.blockHash, 32).hex()[::-1]
        self.bits = self.bits.hex()