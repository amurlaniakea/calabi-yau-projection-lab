# Classroom Lab Sheet / Ficha de Laboratorio

## Target

Undergraduate courses in linear algebra, geometry, topology,
mathematical physics and scientific visualization.
Advanced high-school STEM classes can use Parts 1 to 3.

## Duration

60 to 90 minutes.

## Prerequisites

- vectors, dot product, norm, orthogonality;
- basic complex numbers;
- a browser for the demo, or Python 3 for the CLI.

## Materials

- demo: https://amurlaniakea.github.io/calabi-yau-projection-lab/
- CLI: make test, make examples, projection_lab.cli
- this sheet and a notebook.

## Part 1 — What is a projection? (10 min)

Open the demo. Select Hypercube (R^6).

Observe: the 6D grid becomes a 2D cloud.

Questions:

1. Did the object change? No. What changed? The chosen 2-plane (the camera).
2. How many coordinates are hidden? 6 - 2 = 4.
3. Can two different 6D points land on the same 2D pixel? Yes.
   What does that imply for interpretation?

Key sentence for the board:

    A projection is a shadow, not a photograph.

## Part 2 — Compare cameras with the Seed slider (15 min)

Use the Seed slider (1 to 99) or the Regenerate button,
which advances the seed by one.

Task:

1. Keep Object = Hypercube, Seed = 17. Sketch the silhouette.
2. Set Seed = 18. Sketch again.
3. Repeat for Seed = 42.

Questions:

- Which features are stable across seeds? Which are not?
- Why does the same seed reproduce the same image? (determinism)
- If a paper shows only one projection, what metadata must it report?
  (object, dim, seed, basis seed, points, color mode)

## Part 3 — Clifford torus: a surface in 4D (15 min)

Select Clifford torus (R^4).

The parametrization is:

    T(u,v) = (r cos u, r sin u, r cos v, r sin v), r = 1/sqrt(2)

Tasks:

1. Explain why every point satisfies x1^2 + x2^2 + x3^2 + x4^2 = 1,
   that is, why the torus lies on S^3.
2. Switch Color by = radius. The coloring is nearly uniform. Why?
3. Switch Color by = coordinate 2. What structure appears?

Questions:

- Why is this torus not the donut you see in 3D?
- What does S^1 x S^1 mean as a product of spaces?
- What information does the 2D projection hide here?

## Part 4 — Fermat patches and degree (15 min)

Select Calabi-Yau-like Fermat patch. Set Degree = 3, 4, 5, 6.

The equation is z1^n + z2^n = 1, with n^2 phase patches.

Tasks:

1. Count lobes for n=3 (expect 9 patches) and n=5 (expect 25).
2. Record how the silhouette changes with degree.
3. Explain in one sentence why this patch is NOT a full
   Calabi-Yau threefold.

Expected answer: it is a complex curve (real 2D surface in R^4),
while a CY threefold has real dimension 6.

## Part 5 — Exact topology with the CLI (15 min)

Run:

    PYTHONPATH=src python3 -m projection_lab.cli topology --degree 5 --ambient 4
    PYTHONPATH=src python3 -m projection_lab.cli topology --degree 4 --ambient 3
    PYTHONPATH=src python3 -m projection_lab.cli topology --degree 3 --ambient 2
    PYTHONPATH=src python3 -m projection_lab.cli topology --degree 3 --ambient 3

Table to fill:

| object | h11 | other | chi | CY? |
|---|---|---|---|---|
| quintic in CP4 | 1 | h21=101 | -200 | yes |
| quartic K3 | 20 | h20=1 | 24 | yes |
| elliptic cubic | 1 | h10=1 | 0 | yes |
| cubic surface | 7 | h20=0 | 9 | no |

Questions:

- Why is chi = 2(h11 - h21) for a threefold?
- Why does the code double off-diagonal Hodge entries?
  (symmetry h^{p,q} = h^{q,p})
- What does exact integer combinatorics guarantee that a
  floating-point computation would not?

## Part 6 — Slices as tomography (10 min)

CLI:

    PYTHONPATH=src python3 -m projection_lab.cli slice --dim 6 --steps 8 --fixed 3=0.0,4=0.0 --seed 10 --out examples/slice00.svg
    PYTHONPATH=src python3 -m projection_lab.cli slice --dim 6 --steps 8 --fixed 3=0.5,4=0.5 --seed 10 --out examples/slice55.svg

Questions:

- What does freezing a coordinate mean geometrically?
- Compare with medical CT: what is a slice of a 6D object?
- Which coordinates are still hidden after the slice?

## Assessment

1. In three sentences, explain why a 2D image of a 6D object
   is not the object.
2. Given two projections of the same hypercube with seeds 17 and 18,
   list what is identical and what differs.
3. Compute by hand chi for the quintic from h11=1, h21=101
   and explain the sign.
4. Show that the Clifford torus with r=1/sqrt(2) lies on S^3.
5. State one thing this repository does NOT do and why that
   limitation is documented.

## Rubric

- understands projection as a linear map: 20 percent
- identifies lost information and hidden coordinates: 20 percent
- connects Clifford torus to S^3 and product geometry: 20 percent
- uses exact topology values correctly: 20 percent
- respects explicit limitations (no physics claims): 20 percent

## Part 7 — Quintic branch explorer (15 min)

Open the demo and select Quintic CY3 chart (R^8).

The affine chart is:

    z0^5 + z1^5 + z2^5 + z3^5 + 1 = 0

with:

    z3 = (-1 - z0^5 - z1^5 - z2^5)^(1/5)

There are five branches, labeled 0 to 4.

Tasks:

1. Set Branch = 0. Record max residual and discarded points from Render data.
2. Change Branch = 1. Observe how the projected cloud changes.
3. Repeat for Branch = 2, 3, 4.
4. Keep Seed fixed while changing Branch. What changes? What stays the same?
5. Switch Color by = coordinate 2 or last coordinate. Which hidden structure becomes visible?

Questions:

- Why do different branches give different z3 values?
- Why is a single branch not the whole quintic threefold?
- What does the residual check prove about the sampled points?
- If discarded points are zero or very small, what does that say about numerical consistency?
- How does this connect to exact topology values h11=1, h21=101, chi=-200?

Important interpretation:

- Branch changes the local sheet of the algebraic equation.
- Seed changes the projection camera.
- The mathematical object is not the 2D image.
- No metric or Ricci-flatness is being computed here.

## Resumen en espanol

Ficha de 60 a 90 minutos para aulas de algebra lineal, geometria,
topologia y visualizacion cientifica.

Partes: proyeccion como sombra; camara con el slider Seed;
toro de Clifford en S^3; parches de Fermat y grado;
topologia exacta por CLI; slices como tomografia.

Evaluacion: explicar perdidas de informacion, comparar semillas,
calcular chi de la quintica, verificar Clifford en S^3
y enunciar limites del repo.
Nota en espanol: la Parte 7 pide comparar las cinco ramas locales del chart afine de la quintica, registrar el residuo maximo y distinguir entre cambio de rama (hoja local) y cambio de seed (camara de proyeccion).
