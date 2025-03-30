import time
from Blockchain.Backend.util.util import decode_base58
from Blockchain.Backend.core.Script import Script
from Blockchain.Backend.core.Tx import TxIn, TxOut, Tx
from Blockchain.Backend.core.database.database import AccountDB
from Blockchain.Backend.core.EllepticCurve.EllepticCurve import PrivateKey

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
    
    def getPrivateKey(self):
        AllAccounts = AccountDB().read()
        for account in AllAccounts:
            if account['PublicAddress'] == self.FromPublicAddress:
                return account['privateKey']
        return False

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

        for Txbyte in newutxos:
            if self.Total < self.Amount:
                TxObj = newutxos[Txbyte]

                for index, txout in enumerate(TxObj.tx_outs):
                    if txout.script_pubkey.cmds[2] == self.fromPubKeyHash:
                        self.Total += txout.amount
                        prev_tx = bytes.fromhex(TxObj.id())
                        TxIns.append(TxIn(prev_tx, index))
            else:
                break
        
        self.isBalanceEnough = True

        if self.Total < self.Amount:
            self.isBalanceEnough = False
        
        return TxIns

    def prepareTxOut(self):
        TxOuts = []
        to_scriptPubkey = self.scriptPubKey(self.toAccount)
        TxOuts.append(TxOut(self.Amount, to_scriptPubkey))

        """Calculate fee"""
        self.fee = self.COIN
        self.changeAmount = self.Total - self.Amount - self.fee

        TxOuts.append(TxOut(self.changeAmount, self.From_address_script_pubkey))
        return TxOuts
    
    def signTx(self):
        secret = self.getPrivateKey()
        priv = PrivateKey(secret=secret)

        for index, input in enumerate(self.TxIns):
            self.TxObj.sign_input(index, priv, self.From_address_script_pubkey)

        return True

    def prepareTransaction(self):
        self.TxIns = self.prepareTxIn()

        if self.isBalanceEnough:
            self.TxOuts = self.prepareTxOut()
            self.TxObj = Tx(1, self.TxIns, self.TxOuts, 0)
            self.TxObj.TxId = self.TxObj.id()
            self.signTx()
            return self.TxObj
        
        return False