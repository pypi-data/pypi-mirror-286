# secp256k1_nlg.py
# license: MIT
# This script implements secp256k1 elliptic curve key pair generation using the custom NLGdecimal number system.

import random
from src.nmal import decimal_to_nlgmal
from src.neccak import neccak256

# secp256k1 curve parameters
CURVE_P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
CURVE_A = 0
CURVE_B = 7
CURVE_Gx = 0x79BE667EF9DCBBAC55A06295CE870B70A0C6F14F1E8F2F0D5E4E8D0F4D8C8A8
CURVE_Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B
CURVE_N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
CURVE_H = 1

def mod_inverse(a, p):
    """Compute the modular inverse of a modulo p."""
    return pow(a, p - 2, p)

def point_add(P, Q, curve_p):
    """Add two points P and Q on the secp256k1 curve."""
    if P == (0, 0):
        return Q
    if Q == (0, 0):
        return P
    (x1, y1) = P
    (x2, y2) = Q
    if x1 == x2 and y1 != y2:
        return (0, 0)
    if x1 == x2:
        m = (3 * x1 * x1 + CURVE_A) * mod_inverse(2 * y1, curve_p) % curve_p
    else:
        m = (y2 - y1) * mod_inverse(x2 - x1, curve_p) % curve_p
    x3 = (m * m - x1 - x2) % curve_p
    y3 = (m * (x1 - x3) - y1) % curve_p
    return (x3, y3)

def scalar_mult(k, point, curve_p):
    """Multiply a point by a scalar k on the secp256k1 curve."""
    result = (0, 0)
    addend = point
    while k:
        if k & 1:
            result = point_add(result, addend, curve_p)
        addend = point_add(addend, addend, curve_p)
        k >>= 1
    return result

def generate_keypair():
    """Generate a secp256k1 key pair."""
    priv_key = random.getrandbits(256) % CURVE_N
    pub_key = scalar_mult(priv_key, (CURVE_Gx, CURVE_Gy), CURVE_P)
    return priv_key, pub_key

def private_key_to_nlg256(priv_key):
    """Convert a private key to NLG256 format."""
    return decimal_to_nlgmal(priv_key)

def public_key_to_nlg256(pub_key):
    """Convert a public key to NLG256 format."""
    x, y = pub_key
    return decimal_to_nlgmal(x) + decimal_to_nlgmal(y)

def address_from_public_key(pub_key):
    """Generate an address from a public key."""
    pub_key_bytes = pub_key[0].to_bytes(32, 'big') + pub_key[1].to_bytes(32, 'big')
    hashed_pub_key = neccak256(pub_key_bytes)
    address = hashed_pub_key[-40:]  # Take the last 20 bytes (40 hex characters)
    return address


