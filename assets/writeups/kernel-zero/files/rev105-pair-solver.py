#!/usr/bin/env python3
"""Recover the chained printable characters described in the rev105 write-up.

Pass the sum, low-byte product and XOR arrays copied from Ghidra as three
comma-separated integer lists.  The script implements the exact constraints
recorded in the source document; it does not depend on a hard-coded flag.
"""

import sys


def values(argument):
    return [int(value, 0) for value in argument.split(",") if value]


def candidates(total, product, xor_value):
    return [
        (left, right)
        for left in range(32, 127)
        for right in range(32, 127)
        if left + right == total
        and (left * right) & 0xFF == product
        and left ^ right == xor_value
    ]


def main():
    if len(sys.argv) != 4:
        raise SystemExit(
            "Usage: rev105-pair-solver.py sums products xors\n"
            "Example: rev105-pair-solver.py 0x..,0x.. 0x..,0x.. 0x..,0x.."
        )

    sums, products, xors = map(values, sys.argv[1:])
    if not (len(sums) == len(products) == len(xors)):
        raise SystemExit("The three arrays must have the same length.")

    pairs = [candidates(*triple) for triple in zip(sums, products, xors)]
    if any(not pair for pair in pairs):
        raise SystemExit("No printable pair matches at least one array entry.")

    for first, second in pairs[0]:
        output = [first, second]
        for options in pairs[1:]:
            next_values = [right for left, right in options if left == output[-1]]
            if not next_values:
                break
            output.append(next_values[0])
        else:
            if output[-1] == output[0]:
                print(bytes(output[:-1]).decode())


if __name__ == "__main__":
    main()
