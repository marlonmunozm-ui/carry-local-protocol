#!/usr/bin/env python3
"""
Cross-validation of the Verilog carry_chain output against a Python
big-integer reference.

Usage:
    iverilog -o tb tb_comparison.v
    vvp tb > output.txt
    python cross_validate.py output.txt
"""
import sys
import re


def parse_csv_blocks(filename):
    blocks = []
    current = None
    with open(filename) as f:
        for line in f:
            line = line.strip()
            m = re.match(r"CSV_START seed=([0-9a-fA-F]+) N=(\d+) W=(\d+) carry_out=(\d)", line)
            if m:
                current = {"seed": m.group(1), "N": int(m.group(2)),
                           "W": int(m.group(3)), "carry_out": int(m.group(4)),
                           "words": []}
                continue
            if line.startswith("CSV,") and current is not None:
                parts = line.split(",")
                current["words"].append((int(parts[1]),
                                         int(parts[2], 16),
                                         int(parts[3], 16),
                                         int(parts[4], 16)))
            if line == "CSV_END" and current is not None:
                blocks.append(current)
                current = None
    return blocks


def verify_block(block):
    W, N = block["W"], block["N"]
    B = 1 << W
    A = sum(w[1] * (B ** i) for i, w in enumerate(block["words"]))
    Bn = sum(w[2] * (B ** i) for i, w in enumerate(block["words"]))
    D = sum(w[3] * (B ** i) for i, w in enumerate(block["words"]))
    expected = A + Bn
    D_with_carry = D + (block["carry_out"] * (B ** N))
    return expected, D_with_carry


def main():
    if len(sys.argv) < 2:
        print("Usage: python cross_validate.py output.txt")
        sys.exit(1)

    blocks = parse_csv_blocks(sys.argv[1])
    print(f"Parsed {len(blocks)} CSV blocks from {sys.argv[1]}\n")

    fails = 0
    for i, block in enumerate(blocks):
        expected, D_with_carry = verify_block(block)
        ok = (expected == D_with_carry)
        status = "PASS" if ok else "FAIL"
        print(f"Run {i+1} (seed=0x{block['seed']}): {status}  "
              f"A+B = {expected}, D+carry = {D_with_carry}")
        if not ok:
            fails += 1

    print(f"\nTotal: {len(blocks) - fails}/{len(blocks)} passed")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
