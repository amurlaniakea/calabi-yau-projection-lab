# Equations, Clifford Torus and PSM Note

## 1. Orthogonal projection

Given x in R^n and an orthonormal 2-plane basis u1,u2:

    pi(x) = (<x,u1>, <x,u2>) in R^2

The seed chooses the basis. The object does not change; the camera changes.

## 2. Clifford torus

The Clifford torus is a smooth 2D surface in R^4:

    T(u,v) = (r cos u, r sin u, r cos v, r sin v)

with u,v in [0,2pi). For r = 1/sqrt(2):

    x1^2 + x2^2 + x3^2 + x4^2 = 1

so T lies on S^3. It is S^1 x S^1.

Pedagogical value: product geometry, embedding, hidden coordinates, projection loss.

## 3. Fermat patch implemented by cy-patch

The CLI object cy-patch uses:

    z1^n + z2^n = 1

with z1,z2 complex. In real coordinates:

    (Re(z1), Im(z1), Re(z2), Im(z2)) in R^4

This is a complex curve, equivalently a real 2D surface in 4D. It has n^2 phase patches.

Important: it is not a full Calabi-Yau threefold.

## 4. Quintic Calabi-Yau threefold

The standard quintic CY3 is:

    Z0^5 + Z1^5 + Z2^5 + Z3^5 + Z4^5 = 0

inside CP^4. It has complex dimension 3 and real dimension 6.

Known exact invariants:

    h^{1,1} = 1
    h^{2,1} = 101
    chi = 2(h^{1,1} - h^{2,1}) = -200

The Python topology module stores these as exact integers. It does not compute the metric.

## 5. Euler characteristic from Hodge numbers

For a compact Kahler manifold:

    chi = sum_{p,q} (-1)^(p+q) h^{p,q}

Because h^{p,q}=h^{q,p}, the implementation doubles off-diagonal terms and keeps diagonal terms once.

## 6. PSM note

Here PSM is interpreted as pseudo-spectral method, a possible future numerical layer for Calabi-Yau metrics.

The geometric problem is to find a Kahler potential phi such that the metric is Ricci-flat. In local form this leads to a complex Monge-Ampere type equation:

    (omega + i partial partial-bar phi)^3 = exp(f) omega^3

This is not implemented in the zero-dependency core. A future sibling repository could use NumPy/SciPy/JAX or ML methods. This repository remains the clean educational and reproducible projection core.

## 7. Classroom interpretation checklist

For every image, ask:

1. What is the original dimension?
2. What object was sampled?
3. What seed defined the projection plane?
4. What coordinate is encoded as color?
5. What information was lost?
6. Is this a full object, a patch, a slice or a sampled domain?
