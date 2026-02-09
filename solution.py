from math import factorial

def solve(n_arcs):
    p = n_arcs // 5
    total = 0
    for r in range(p + 1):
        l = p - r
        s = r * l
        T0 = p**4 - 3 * p**2 * s + s**2
        num = p * T0 * factorial(p - 1) ** 5
        den = factorial(r) ** 5 * factorial(l) ** 5
        total += num // den
    return total

print(solve(70))  # 331951449665644800
