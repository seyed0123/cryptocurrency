class EllipticCurve:

    def __init__(self, a, b, p):
        # y^2 = x^3 + ax + b (mod p)
        self.a = a % p
        self.b = b % p
        self.p = p

    def scalar_multiplication(self, k, P):
        if k==0 or P is None:
            return None
        
        result = None
        for _ in range(k):
            result = self.add_points(result,P)
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

class ECDH:

    def __init__(self, curve:EllipticCurve, base_point, private_key, other_public_key=None):
    # curve is EllipticCurve instance
       self.curve = curve
       self.base_point = base_point
       self.private_key = private_key
       if other_public_key:
           self.other_public_key = other_public_key

    def get_public_key(self):
        return self.curve.scalar_multiplication(self.private_key,self.base_point)

    def set_other_public_key(self, other_public_key):
        self.other_public_key = other_public_key

    def get_shared_secret(self):
        return self.curve.scalar_multiplication(self.private_key,self.other_public_key)
    
curve = EllipticCurve(2, 2, 17)
G = (5, 1)
alice_private_key = 3
alice_ecdh = ECDH(curve, G, alice_private_key)
bob_private_key = 5
bob_ecdh = ECDH(curve, G, bob_private_key)
alice_public_key = alice_ecdh.get_public_key()
bob_public_key = bob_ecdh.get_public_key()
alice_ecdh.set_other_public_key(bob_public_key)
bob_ecdh.set_other_public_key(alice_public_key)
alice_shared_secret = alice_ecdh.get_shared_secret()
bob_shared_secret = bob_ecdh.get_shared_secret()

print(alice_shared_secret)
print(bob_shared_secret)
# Two secrets should match