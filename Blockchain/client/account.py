import sys
sys.path.append(r'C:\Users\Shivam\Desktop\crypto-crafter')
from Blockchain.Backend.core.EllepticCurve import Sha256Point

class account:
    def createKeys(self):
        """Secp256k1 Curve Generator Points"""
        Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
        Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8

        G = Sha256Point(Gx, Gy)