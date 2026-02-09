# Project Euler 208 — Robot Walks

## Problem

A robot moves in a series of one-fifth circular arcs (72°), choosing clockwise or
anticlockwise for each step. Starting facing North, how many journeys of 70 arcs
return the robot to its starting position?

## Answer

**331951449665644800**

## Solution

### 1. Direction state on C₅

Each arc turns the robot by 72°, so there are exactly 5 possible facing directions,
which we label 0–4 (with 0 = North). A **right** (clockwise) arc from direction d
moves to direction (d+1) mod 5; a **left** (anticlockwise) arc moves to (d−1) mod 5.

Let R_d and L_d denote the number of right and left arcs taken while facing
direction d.

### 2. Return-to-origin via roots of unity

Place the plane in ℂ. Let ω = e^(2πi/5). A careful computation of the displacement
vector for each arc type shows:

- Right arc from direction d: displacement Δ_R(d) = (1 − ω̄) · ω^(−d)
- Left arc from direction d:  displacement Δ_L(d) = (ω − 1) · ω^(−d)

The total displacement is:

$$\sum_{d=0}^{4} \bigl[ R_d \cdot \Delta_R(d) + L_d \cdot \Delta_L(d) \bigr] = \sum_{d=0}^{4} a_d \, \omega^{-d} = 0$$

where a_d = R_d − L_d − R_{d−1} + L_{d+1}.

Since {1, ω, ω², ω³} form a basis for ℚ(ω) over ℚ, the only way this sum
vanishes is if all a_d are equal — and since they sum to zero, each a_d = 0:

$$R_d - L_d = R_{d-1} - L_{d+1} \quad \text{for all } d \pmod{5}$$

### 3. Combining with flow conservation

The walk must also conserve flow at each vertex (arrivals = departures):

$$R_d + L_d = R_{d-1} + L_{d+1} \quad \text{for all } d \pmod{5}$$

Adding and subtracting the two conditions:

- **R_d = R_{d−1}** for all d  ⟹  R₀ = R₁ = R₂ = R₃ = R₄ ≡ r
- **L_d = L_{d+1}** for all d  ⟹  L₀ = L₁ = L₂ = L₃ = L₄ ≡ l

So the right-arc and left-arc counts must be **uniform across all 5 directions**.

With 70 total arcs: 5(r + l) = 70, giving **r + l = 14**.

The direction returns to North automatically since the net direction change
5r − 5l ≡ 0 (mod 5).

### 4. Counting walks via the BEST theorem

For a given (r, l), the problem is equivalent to counting **Eulerian circuits** in
a directed multigraph M on the 5-cycle, where each vertex has r forward edges and
l backward edges (70 edges total, out-degree = in-degree = 14 at every vertex).

The **BEST theorem** (de Bruijn, van Aardenne-Ehrenfest, Smith, Tutte) states that
the number of labelled Eulerian circuits from a fixed vertex with a fixed first edge
in a connected balanced directed graph is:

$$T_w \times \prod_{v} (d^+(v) - 1)!$$

where T_w is the number of arborescences rooted at w.

Accounting for all first-edge choices and dividing out edge-label permutations
(since we only distinguish R vs L, not which specific copy of a parallel edge is
used), the number of distinct R/L sequences is:

$$\text{Count}(r, l) = 14 \times T_0 \times (13!)^5 \;\big/\; (r!)^5 \cdot (l!)^5$$

### 5. Computing T₀ via the Matrix Tree Theorem

T₀ is the determinant of the reduced Laplacian (delete row 0, column 0) of M.
The out-Laplacian of M restricted to vertices {1, 2, 3, 4} is tridiagonal:

```
⎡ 14  -r   0   0 ⎤
⎢ -l  14  -r   0 ⎥
⎢  0  -l  14  -r ⎥
⎣  0   0  -l  14 ⎦
```

Its determinant satisfies the recurrence D_n = 14·D_{n−1} − rl·D_{n−2}, yielding:

$$T_0 = D_4 = 14^4 - 3 \cdot 14^2 \cdot rl + (rl)^2 = 38416 - 588\,rl + r^2 l^2$$

### 6. Final summation

$$\boxed{\text{Answer} = \sum_{r=0}^{14} \frac{14 \times (38416 - 588\,rl + r^2 l^2) \times (13!)^5}{(r!)^5 \cdot ((14-r)!)^5}}$$

### 7. Verification

For 25 arcs (p = 5), the formula gives 70932, matching the value stated in the
problem.

## Code

```python
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
```
