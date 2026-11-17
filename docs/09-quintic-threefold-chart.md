# Quintic Threefold Affine Chart

## Mathematical object

The quintic Calabi-Yau threefold is the hypersurface:

    Z0^5 + Z1^5 + Z2^5 + Z3^5 + Z4^5 = 0

inside complex projective space CP^4.

It has:

    complex dimension = 3
    real dimension = 6

This is the object most commonly discussed in string theory
compactification.

## Affine chart implemented

We work in the chart Z4 = 1, so the equation becomes:

    z0^5 + z1^5 + z2^5 + z3^5 + 1 = 0

We parametrize (z0, z1, z2) on a polar grid in the disk
|z| <= radius_max, and solve:

    z3 = (-1 - z0^5 - z1^5 - z2^5)^(1/5)

There are 5 branches of the 5th root. The --branch parameter
selects one of them (0 to 4).

Each point is stored in R^8:

    (Re z0, Im z0, Re z1, Im z1, Re z2, Im z2, Re z3, Im z3)

## Residual check

For every generated point, the code verifies:

    |z0^5 + z1^5 + z2^5 + z3^5 + 1| < 1e-9

Points failing this check are discarded. The test suite
asserts this residual bound.

## Branch normalization

The complex root uses atan2 and normalizes the angle to [0, 2pi)
before dividing by 5. This avoids signed-zero artifacts that could
make two branches appear identical in one coordinate while differing
in another.

The test suite compares the full complex z3 value, not just its real
part, to verify branch separation.

## Limitations

- This is a LOCAL chart, not the global variety.
- It does not cover points where Z4 = 0.
- Five branches give five local patches, not a global atlas.
- The projection R^8 -> R^2 loses 6 dimensions of information.
- Color encodes one hidden coordinate; it is an interpretation.
- No metric is computed. No Ricci-flatness is verified.
- No cohomology is computed from scratch.
- Hodge numbers (h11=1, h21=101, chi=-200) are exact integer
  combinatorics from the topology module, not derived from
  this chart.

## Pedagogical value

- Shows a real 6D object (complex 3-fold) embedded in R^8.
- Demonstrates branch selection in complex roots.
- Provides a residual check as evidence of algebraic correctness.
- Connects to the quintic CY3 used in physics, without claiming
  to simulate physics.
- Useful for comparing projections across branches and seeds.

## CLI usage

    PYTHONPATH=src python3 -m projection_lab.cli quintic-chart \
      --grid 4 --branch 0 --seed 6 \
      --out examples/quintic_chart_g4_b0.svg \
      --meta examples/quintic_chart_g4_b0.json

Compare branches:

    PYTHONPATH=src python3 -m projection_lab.cli quintic-chart \
      --grid 4 --branch 0 --seed 6 \
      --out examples/quintic_chart_b0.svg

    PYTHONPATH=src python3 -m projection_lab.cli quintic-chart \
      --grid 4 --branch 1 --seed 6 \
      --out examples/quintic_chart_b1.svg

Same object, different local patch. The projected image changes
because z3 differs by a 5th root of unity factor.

## Relation to topology module

The topology module provides exact Hodge numbers for the quintic:

    h^{1,1} = 1
    h^{2,1} = 101
    chi = -200

These are classification data. The chart provides a geometric
realization of a local piece of the same variety. They are
complementary, not redundant.
