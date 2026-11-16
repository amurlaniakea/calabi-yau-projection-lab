# Degree, Patches and Calabi-Yau Clarification

## The implemented Fermat patch

The current cy-patch object is based on a Fermat-type complex
equation:

    z1^n + z2^n = 1

with z1, z2 in C.

Represented in real coordinates, each point lives in:

    R^4 = (Re(z1), Im(z1), Re(z2), Im(z2))

This is a complex curve, equivalently a real 2-dimensional surface
embedded in 4D.

It is NOT a full Calabi-Yau threefold.

## Why n^2 patches appear

The equation z1^n + z2^n = 1 can be parametrized using nth-root
phases.

For each choice of phase for z1 and each choice of phase for z2,
one obtains a local patch.

Since there are n choices for each coordinate, the number of
patches is:

    n * n = n^2

Examples:

    n = 3 -> 9 patches
    n = 4 -> 16 patches
    n = 5 -> 25 patches

Visually, increasing n produces more symmetric lobes or petals
in the projected image.

## Relation to the quintic Calabi-Yau threefold

The famous quintic Calabi-Yau threefold is NOT:

    z1^5 + z2^5 = 1

It is:

    Z0^5 + Z1^5 + Z2^5 + Z3^5 + Z4^5 = 0

inside complex projective space CP^4.

This variety has:

    complex dimension = 3
    real dimension = 6

That is the object commonly used in string compactification
discussions.

## Why degree 5 is special

For a smooth hypersurface in CP^m, the canonical bundle is trivial
when the degree is m + 1.

For CP^4:

    m = 4
    degree = 5

Therefore the quintic hypersurface in CP^4 is a Calabi-Yau threefold.

This is a deeper reason than it has 25 patches.

## Pedagogical warning

When showing images from cy-patch, one should say:

> This is a Fermat-type Calabi-Yau-like patch, a smooth complex
> curve in 4D projected to 2D. It is not a full 6D Calabi-Yau
> threefold.

This avoids misleading students and researchers.

## Exact Hodge numbers (topology module)

The topology module provides exact integer Hodge numbers for
known Fermat hypersurfaces:

    (3, 2): elliptic curve, h^{1,0}=1, chi=0
    (4, 3): quartic K3, h^{2,0}=1, h^{1,1}=20, chi=24
    (5, 4): quintic CY3, h^{1,1}=1, h^{2,1}=101, chi=-200
    (3, 3): cubic surface (NOT CY), h^{1,1}=7

These are classification data, not metric computations.

## Future physics-oriented object

A more physics-relevant object would be a local chart of the
quintic threefold:

    z0^5 + z1^5 + z2^5 + z3^5 + 1 = 0

using:

    z3 = (-1 - z0^5 - z1^5 - z2^5)^(1/5)

This would provide a 6-real-dimensional local chart, suitable for
projection and future metric diagnostics.
