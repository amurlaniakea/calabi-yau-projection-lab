.PHONY: test examples clean

test:
	PYTHONPATH=src python3 -m unittest discover -s tests -p 'test_*.py' -v

examples:
	mkdir -p examples
	PYTHONPATH=src python3 -m projection_lab.cli cube --dim 6 --steps 4 --seed 1 --out examples/cube6d_seed1.svg --meta examples/cube6d_seed1.json
	PYTHONPATH=src python3 -m projection_lab.cli domain --dim 11 --samples 2500 --seed 2 --out examples/domain11d_seed2.svg --meta examples/domain11d_seed2.json
	PYTHONPATH=src python3 -m projection_lab.cli cy-patch --degree 5 --resolution 14 --seed 3 --out examples/cy_patch_d5_r14.svg --meta examples/cy_patch_d5_r14.json
	PYTHONPATH=src python3 -m projection_lab.cli slice --dim 6 --steps 6 --fixed 3=0.25,4=0.75 --seed 4 --out examples/slice6d_seed4.svg --meta examples/slice6d_seed4.json
	PYTHONPATH=src python3 -m projection_lab.cli clifford-torus --samples-u 48 --samples-v 48 --seed 5 --out examples/clifford_torus_seed5.svg --meta examples/clifford_torus_seed5.json
	PYTHONPATH=src python3 -m projection_lab.cli quintic-chart --grid 4 --branch 0 --seed 6 --out examples/quintic_chart_g4_b0.svg --meta examples/quintic_chart_g4_b0.json

clean:
	find . -type d -name '__pycache__' -exec rm -rf {} +
	rm -f examples/*.svg examples/*.json

quintic-gallery:
	PYTHONPATH=src python3 -m projection_lab.cli quintic-chart --grid 4 --branch 0 --seed 6 --out examples/quintic_branch0.svg --meta examples/quintic_branch0.json
	PYTHONPATH=src python3 -m projection_lab.cli quintic-chart --grid 4 --branch 1 --seed 6 --out examples/quintic_branch1.svg --meta examples/quintic_branch1.json
	PYTHONPATH=src python3 -m projection_lab.cli quintic-chart --grid 4 --branch 2 --seed 6 --out examples/quintic_branch2.svg --meta examples/quintic_branch2.json
	PYTHONPATH=src python3 -m projection_lab.cli quintic-chart --grid 4 --branch 3 --seed 6 --out examples/quintic_branch3.svg --meta examples/quintic_branch3.json
	PYTHONPATH=src python3 -m projection_lab.cli quintic-chart --grid 4 --branch 4 --seed 6 --out examples/quintic_branch4.svg --meta examples/quintic_branch4.json

quintic-gallery-previews:
	mkdir -p docs/assets/quintic_branches
	PYTHONPATH=src python3 -m projection_lab.cli quintic-chart --grid 3 --branch 0 --seed 6 --out docs/assets/quintic_branches/branch0.svg --meta docs/assets/quintic_branches/branch0.json
	PYTHONPATH=src python3 -m projection_lab.cli quintic-chart --grid 3 --branch 1 --seed 6 --out docs/assets/quintic_branches/branch1.svg --meta docs/assets/quintic_branches/branch1.json
	PYTHONPATH=src python3 -m projection_lab.cli quintic-chart --grid 3 --branch 2 --seed 6 --out docs/assets/quintic_branches/branch2.svg --meta docs/assets/quintic_branches/branch2.json
	PYTHONPATH=src python3 -m projection_lab.cli quintic-chart --grid 3 --branch 3 --seed 6 --out docs/assets/quintic_branches/branch3.svg --meta docs/assets/quintic_branches/branch3.json
	PYTHONPATH=src python3 -m projection_lab.cli quintic-chart --grid 3 --branch 4 --seed 6 --out docs/assets/quintic_branches/branch4.svg --meta docs/assets/quintic_branches/branch4.json

metric-diag:
	PYTHONPATH=src python3 -m projection_lab.cli metric-diag --grid 3 --branch 0 --seed 6 --sample 50 --meta examples/metric_diag_quintic_g3_b0.json
