# 1
To find the irreducible polynomials over GF(2) do this in the code:
- The polynomials are represented as integers, with each bit indicating whether a term of a particular degree is present.
- The gf2_divmod function performs polynomial division over GF(2) using bitwise operations, mimicking the long division process. It repeatedly aligns the divisor with the dividend and subtracts (XORs) it until the degree of the remaining dividend becomes less than that of the divisor.
- The is_irreducible function checks whether a given polynomial is irreducible by trying to divide it by all polynomials of smaller degree starting from 2 (to avoid trivial cases). If any of these lower-degree polynomials divide the input without a remainder, the polynomial is reducible. Otherwise, it is added to the list by list_irreducibles, which scans through all polynomials in the given degree range.
- the poly_to_str function converts the binary representation of each irreducible polynomial into a human-readable algebraic form (e.g., x^4 + x + 1). 

and this is the result of running the code

```txt
0b1011: x^3 + x + 1
0b1101: x^3 + x^2 + 1
0b10011: x^4 + x + 1
0b11001: x^4 + x^3 + 1
0b11111: x^4 + x^3 + x^2 + x + 1
```

Each of these polynomials has been verified by the code to be irreducible over GF(2), meaning they cannot be factored into lower-degree polynomials within the same field.

# 2

This is the featues of this hash func:
1. **Collision Resistance (CR):**
   If the **Discrete Logarithm Problem (DLP)** is hard in the group $\mathbb{Z}_p^*$, and $A, B$ are independent generators (i.e., no one knows the discrete log between them), then this function is **computationally collision-resistant**. That means it's hard to find $(x_1, x_2) \neq (x_1', x_2')$ such that:

   $$
   A^{x_1} \cdot B^{x_2} \equiv A^{x_1'} \cdot B^{x_2'} \pmod{p}
   $$

2. **Linearity:**
   The function is **homomorphic**:

   $$
   H(x_1 + x_1', x_2 + x_2') = H(x_1, x_2) \cdot H(x_1', x_2')
   $$

   This can be a **feature** (e.g., in zero-knowledge proofs or commitments) but **not good** if you want a traditional cryptographic hash, because it leaks structure.

3. **Not Preimage Resistant Without Constraints:**
   If $A$ and $B$ are known and public, and the domain of $x_1, x_2$ is small, an attacker can **brute force** possible values. So it should be used with **large enough inputs**.

4. **Discrete Log Relation Between A and B Must Be Unknown:**
   If $B = A^b$, and someone knows $b$, then they can compute:

   $$
   A^{x_1} \cdot B^{x_2} = A^{x_1 + b x_2}
   $$

   Reducing the function to a single-exponent value, making collision finding easier.

## Code
The code begins by initializing parameters: a safe prime $p = 23$, $q = (p-1)/2$, a generator $A = 5$, and a secret exponent $b_{\text{secret}}$ chosen randomly to compute $B = A^{b_{\text{secret}}} \mod p$.The core of the hash function is the `round_hash` function, which takes two inputs $x_1$ and $x_2$ from the subgroup $\mathbb{Z}_q$, computes $A^{x_1}$ and $B^{x_2}$, and returns their product modulo $p$. This operation leverages the algebraic properties of the group to mix the inputs securely.

To process arbitrary-length input data, the function `bytes_to_blocks` splits the byte stream into pairs $(x_1, x_2)$, ensuring each value is reduced modulo $q$ to stay within the subgroup. The `merkle_damgard_hash` function initializes a chaining value $h$ and iteratively updates it by XORing the first component of each block with the current state $h$ and then applying the `round_hash`.

And this is an example usage of the code
```txt
Hash of 'hello world': 10
```
# 3
 A custom Python class is developed to model elliptic curve operations, including point addition and scalar multiplication. The curve used is defined by the equation $y^2 = x^3 + 171x + 853 \mod 2671$, and all computations are performed modulo 2671. The class handles cases such as point doubling and inverse modulo operations. Using this setup, we simulate the ECDH process: Alice shares the point $Q_A = (2110, 543)$, and Bob computes $1943 \cdot Q_A = (2424, 911)$. Meanwhile, Bob sends $(1432, 667)$ as $n_B \cdot P$, allowing Alice to compute the same shared secret.

In the second part of the protocol, Bob chooses a point with $x = 2$. Solving the curve equation for $y$ gives two possibilities: $y = 96$ or $2575$, so the point could be $(2, 96)$ or $(2, 2575)$. Bob uses $(2, 2575)$ and multiplies it by his private scalar $n = 875$, resulting in the point $(161, 2040)$, of which only the x-coordinate is sent to Alice. Since two points can share the same x-coordinate, Bob considers both resulting secrets: $(1708, 1252)$ and $(1708, 1419)$. The shared secret is then inferred to be the x-coordinate $1708$. This implementation shows how ECDH securely establishes a shared key over an insecure channel using elliptic curves.

# 