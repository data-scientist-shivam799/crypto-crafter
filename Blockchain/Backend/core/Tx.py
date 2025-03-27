from Blockchain.Backend.core.Script import Script
from Blockchain.Backend.util.util import hash256, int_to_little_endian, little_endian_to_int, bytes_needed, decode_base58, encode_varint

ZERO_HASH = b'\0' * 32
REWARD = 50

PRIVATE_KEY = '11345201149040514282586684444675963559533682456284054931805066756824897714465'
MINER_ADDRESS = '164kxccHGmAXsqriKzSsJWxcFSJu1VievZ'

class CoinbaseTx:
    def __init__(self, BlockHeight):
        self.BlockHeightInLittleEndian = int_to_little_endian(BlockHeight, bytes_needed(BlockHeight))
    
    def CoinbaseTransaction(self):
        prev_tx = ZERO_HASH
        prev_index = 0xffffffff

        tx_ins = []
        tx_ins.append(TxIn(prev_tx, prev_index))
        tx_ins[0].script_sig.cmds.append(self.BlockHeightInLittleEndian)

        tx_outs = []
        target_amount = REWARD * 100000000
        target_h160 = decode_base58(MINER_ADDRESS) 
        target_script = Script.p2pkh_script(target_h160)
        tx_outs.append(TxOut(amount=target_amount, script_pubkey=target_script))

        coinBaseTx = Tx(1, tx_ins, tx_outs, 0)
        coinBaseTx.TxId = coinBaseTx.id()
        return coinBaseTx

class Tx:
    def __init__(self, version, tx_ins, tx_outs, locktime):
        self.version = version
        self.tx_ins = tx_ins
        self.tx_outs = tx_outs
        self.locktime = locktime
    
    def id(self):
        """Human-readable Tx id"""
        return self.hash().hex()
    
    def hash(self):
        """Binary Hash of Serialization"""
        return hash256(self.serialize())[::-1]

    def serialize(self):
        result = int_to_little_endian(self.version, 4)
        result += encode_varint(len(self.tx_ins))

        for tx_in in self.tx_ins:
            result += tx_in.serialize()

        result += encode_varint(len(self.tx_outs))
        for tx_out in self.tx_outs:
            result += tx_out.serialize()

        result += int_to_little_endian(self.locktime, 4)
        return result

    def is_coinbase(self):
        """
        # Check that there is exactly 1 input
        # grab the first input and check if the prev_tx is b'\x00' * 32
        # check that the first input prev_index is 0xffffffff 
        """
        if len(self.tx_ins) != 1:
            return False
        
        first_input = self.tx_ins[0]
        if first_input.prev_tx != b'\x00' * 32:
            return False
        
        if first_input.prev_index != 0xffffffff:
            return False
        
        return True

    def to_dict(self):
        """
        Convert Coinbase Transaction
        # convert prev_tx Hash in hex from bytes
        # Convert Blockheight in hex which is stored in Script signature
        """
        if self.is_coinbase():
            self.tx_ins[0].prev_tx = self.tx_ins[0].prev_tx.hex()
            self.tx_ins[0].script_sig.cmds[0] = little_endian_to_int(self.tx_ins[0].script_sig.cmds[0])
            self.tx_ins[0].script_sig = self.tx_ins[0].script_sig.__dict__
        
        self.tx_ins[0] = self.tx_ins[0].__dict__

        """
        Convert Transaction Output to dict
        # If there are Numbers we don’t need to do anything
        # If values is in bytes, convert it to hex
        # Loop Through all the TxOut Objects and convert them into dict
        """
        self.tx_outs[0].script_pubkey.cmds[2] = self.tx_outs[0].script_pubkey.cmds[2].hex()
        self.tx_outs[0].script_pubkey = self.tx_outs[0].script_pubkey.__dict__
        self.tx_outs[0] = self.tx_outs[0].__dict__

        return self.__dict__

class TxIn:
    def __init__(self, prev_tx, prev_index, script_sig=None, sequence=0xffffffff):
        self.prev_tx = prev_tx
        self.prev_index = prev_index

        if script_sig is None:
            self.script_sig = Script()
        else:
            self.script_sig = script_sig

        self.sequence = sequence

    def serialize(self):
        result = self.prev_tx[::-1]
        result += int_to_little_endian(self.prev_index, 4)
        result += self.script_sig.serialize()
        result += int_to_little_endian(self.sequence, 4)
        return result

class TxOut:
    def __init__(self, amount, script_pubkey):
        self.amount = amount
        self.script_pubkey = script_pubkey

    def serialize(self):
        result = int_to_little_endian(self.amount, 8)
        result += self.script_pubkey.serialize()
        return result