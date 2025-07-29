def gf2_divmod(a, b):
    deg_b = b.bit_length() - 1
    result = 0
    while a.bit_length() >= b.bit_length():
        shift = a.bit_length() - b.bit_length()
        result ^= (1 << shift)
        a ^= (b << shift)
    return result, a

def is_irreducible(p):
    deg_p = p.bit_length() - 1
    for f in range(2 , 1 <<( deg_p )):
        _, remainder = gf2_divmod(p, f)
        if remainder == 0:
            return False
    return True

def list_irreducibles(min_deg,max_deg):
    irreducibles = []
    for p in range(1 << min_deg, 1 << (max_deg + 1)):
        if is_irreducible(p):
            irreducibles.append(p)
    return irreducibles

def poly_to_str(p):
    terms = []
    for i in range(p.bit_length()):
        if p & (1 << i):
            if i == 0:
                terms.append("1")
            elif i == 1:
                terms.append("x")
            else:
                terms.append(f"x^{i}")
    return " + ".join(reversed(terms))

irreducibles = list_irreducibles(3,4)
for p in irreducibles:
    print(f"{bin(p)}: {poly_to_str(p)}")
