import os
import hashlib

class EllipticCurve:

    def __init__(self, a, b, p):
        # y^2 = x^3 + ax + b (mod p)
        self.a = a % p
        self.b = b % p
        self.p = p

    def scalar_multiplication(self, k, P):
        if k == 0 or P is None:
            return None

        result = None  
        current = P    

        while k > 0:
            if k % 2 == 1:  
                result = self.add_points(result, current)
            current = self.add_points(current, current) 
            k //= 2  

        return result

    def add_points(self,p1,p2):
        if p1 is None:
            return p2
        if p2 is None:
            return p1
        
        x1,y1 = p1
        x2,y2 = p2
        if x1 == x2 and y1 != y2:
            return None
        
        if x1 != x2:
            l = pow(x2-x1,-1,self.p)
            m =  ((y2-y1) * l ) % self.p 

        elif x1 == x2 and y1 == y2:
            l = pow(2*y1,-1,self.p)
            m = ( (3*x1**2+self.a) * l) % self.p   
        

        x3 = (m**2 -x1 -x2) % self.p 
        y3 = (m*(x1-x3)-y1)%self.p
        return (x3,y3)

class ECDSA():
    def __init__(self,private_key=None) -> None:
        # secp256k1 curve: y² = x³ + 7 mod p
        p_secp256k1 = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
        a_secp256k1 = 0
        b_secp256k1 = 7

        
        Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
        Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
        G = (Gx, Gy)
        self.G = G

        self.n_secp256k1 = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

        curve = EllipticCurve(a_secp256k1, b_secp256k1, p_secp256k1)
        self.curve = curve
        if not private_key:
            private_key = self.generate_private_key()
        self.private_key = private_key



    def generate_private_key(self):
        while True:
            priv = int.from_bytes(os.urandom(32), 'big')
            if 1 <= priv < self.n_secp256k1:
                return priv

    def get_public_key(self):
        return self.curve.scalar_multiplication(self.private_key, self.G)

    def sign_message(self, message):
        h = int(hashlib.sha256(message).hexdigest(), 16) % self.n_secp256k1

        while True:
            k = self.private_key
            P = self.curve.scalar_multiplication(k, self.G)
            r = P[0] % self.n_secp256k1
            if r != 0:
                break

        s = (pow(k, -1, self.n_secp256k1) * (h + private_key * r)) % self.n_secp256k1
        return (r, s)

    def verify_signature(self, public_key, message, sig):
        r, s = sig
        if not (1 <= r < self.n_secp256k1 and 1 <= s < self.n_secp256k1):
            return False

        h = int(hashlib.sha256(message).hexdigest(), 16) % self.n_secp256k1
        w = pow(s, -1, self.n_secp256k1)
        u1 = (h * w) % self.n_secp256k1
        u2 = (r * w) % self.n_secp256k1

        P1 = self.curve.scalar_multiplication(u1, self.G)
        P2 = self.curve.scalar_multiplication(u2, public_key)
        P = self.curve.add_points(P1, P2)

        return P[0] % self.n_secp256k1 == r

message = b"Hello, ECDSA!"
ecdsa =ECDSA()
private_key = ecdsa.private_key
public_key = ecdsa.get_public_key()
signature = ecdsa.sign_message(message)
print("Signature valid?", ecdsa.verify_signature(public_key, message, signature))

print("Private key (point):", private_key)
print("Public key (point): ",
      public_key)
print("sign message: ", signature)