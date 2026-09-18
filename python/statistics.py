#!/usr/bin/env python3
"""
Statistical validation of the frontier measure mu(F) = 1/B and
independent Python re-implementation of the carry protocol.
"""
import random


def ripple(a, b, B):
    n = max(len(a), len(b))
    a = a + [0] * (n - len(a))
    b = b + [0] * (n - len(b))
    d, c = [], 0
    for i in range(n):
        t = a[i] + b[i] + c
        d.append(t % B)
        c = t // B
    return d, c


def protocol(a, b, B):
    n = max(len(a), len(b))
    a = a + [0] * (n - len(a))
    b = b + [0] * (n - len(b))
    s = [a[i] + b[i] for i in range(n)]
    case = ['K' if x <= B - 2 else ('G' if x >= B else 'F') for x in s]
    d = [x % B for x in s]
    fout = [0 if c == 'K' else (1 if c == 'G' else None) for c in case]
    cin = 0
    for i in range(n):
        d[i] = (d[i] + cin) % B
        if case[i] == 'F':
            fout[i] = cin
        cin = fout[i]
    return d, cin


def to_int(digits, B):
    v = 0
    for x in reversed(digits):
        v = v * B + x
    return v


def main():
    random.seed(42)
    B = 2 ** 32
    fails = 0
    for _ in range(5):
        for _ in range(60):
            a = [random.randrange(B) for _ in range(60)]
            b = [random.randrange(B) for _ in range(60)]
            d1, c1 = ripple(a, b, B)
            d2, c2 = protocol(a, b, B)
            total = to_int(a, B) + to_int(b, B)
            if not (c1 == c2 and to_int(d1, B) == to_int(d2, B) == total):
                fails += 1
    print("Cross-validation fails:", fails)

    for k in [1, 2, 4, 8, 12, 16]:
        Bk = 2 ** k
        N = 200_000
        fr = sum(1 for _ in range(N)
                 if random.randrange(Bk) + random.randrange(Bk) == Bk - 1)
        print(f"k={k:2d}  empirical mu(F)={fr/N:.6f}  theoretical={1/Bk:.6f}")


if __name__ == "__main__":
    main()
