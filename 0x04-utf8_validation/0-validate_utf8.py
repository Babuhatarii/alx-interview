#!/usr/bin/python3
"""
UTF-8 Validation
"""


def validUTF8(data):
    # Number of bytes in the current UTF-8 character
    n_bytes = 0

    # Masks to check the most significant bits of each byte
    mask1 = 1 << 7  # 10000000
    mask2 = 1 << 6  # 01000000

    for byte in data:
        # Get the binary representation of the byte (8 least significant bits)
        bin_rep = format(byte, '#010b')[-8:]

        # If we are expecting more bytes in this character
        if n_bytes == 0:
            # Count the number of leading 1's
            for bit in bin_rep:
                if bit == '0':
                    break
                n_bytes += 1

            # 1 byte characters
            if n_bytes == 0:
                continue

            # For 2, 3, or 4 byte characters, the first byte must be valid
            if n_bytes == 1 or n_bytes > 4:
                return False
        else:
            # Check that the byte is a valid continuation byte
            if not (byte & mask1 and not (byte & mask2)):
                return False

        n_bytes -= 1

    return n_bytes == 0
