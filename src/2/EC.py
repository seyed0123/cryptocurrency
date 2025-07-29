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
        
a, b, p = 3,7,5
curve = EllipticCurve(a, b, p)
P = (1,0)
for i in [1,2,4,8]:
    print(curve.scalar_multiplication(i, P))
# result = curve.scalar_multiplication(4, P)
# result should be (10, 2). a tuple.
# print(result)