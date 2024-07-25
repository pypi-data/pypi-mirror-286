# nmal.py
# license: MIT
# This script implements a custom number system named "NLG DECIMAL" (shortened to "NLGmal").
# The NLGmal number system uses the characters 0-9 and m-z, making it a base-24 system.
# This script includes functions to convert decimal numbers to NLGmal and vice versa.

# Defining the NLGmal characters
NLGmal_chars = "0123456789mnopqrstuvwxyz"

base = len(NLGmal_chars)

# Dictionary for quick look-up of character values
char_to_value = {char: idx for idx, char in enumerate(NLGmal_chars)}


def decimal_to_nlgmal(decimal):
    """Convert a decimal number to an NLGmal number."""
    if decimal == 0:
        return NLGmal_chars[0]

    nlgmal = ""
    while decimal > 0:
        nlgmal = NLGmal_chars[decimal % base] + nlgmal
        decimal //= base
    return nlgmal


def nlgmal_to_decimal(nlgmal):
    """Convert an NLGmal number to a decimal number."""
    # Check for capital letters and issue a warning
    if any(char.isupper() for char in nlgmal):
        print("Warning: Capital letters detected. Its good to use small small letter. Please be carefull next time :)")
        nlgmal = nlgmal.lower()

    decimal = 0
    for char in nlgmal:
        decimal = decimal * base + char_to_value[char]
    return decimal


