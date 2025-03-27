import time
from Blockchain.Backend.util.util import decode_base58
from Blockchain.Backend.core.Script import Script

class SendBTC:
    def __init__(self, fromAccount, toAccount, Amount, UTXOS):
        self.COIN = 100000000
        self.FromPublicAddress = fromAccount
        self.toAccount = toAccount
        self.Amount = Amount * self.COIN
        self.utxos = UTXOS
    
    def scriptPubKey(self, PublicAddress):
        h160 = decode_base58(PublicAddress)
        script_pubkey = Script().p2pkh_script(h160)
        return script_pubkey

    def prepareTxIn(self):
        TxIns = []
        self.Total = 0

        """COnvert public address into public hash to find tx outs that are locked to this hash"""
        self.From_address_script_pubkey = self.scriptPubKey(self.FromPublicAddress)
        self.fromPubKeyHash = self.From_address_script_pubkey.cmds[2]

        newutxos = {}

        try:
            while len(newutxos) < 1:
                newutxos = dict(self.utxos)
                time.sleep(2)
        except Exception as e:
            print(f"Error in converting the Managed dictionary to Normal dictionary: {e}")

    def prepareTxOut(self):
        pass
    
    def prepareTransaction(self):
        self.prepareTxIn()
        self.prepareTxOut()