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

clean:
	find . -type d -name '__pycache__' -exec rm -rf {} +
	rm -f examples/*.svg examples/*.json
