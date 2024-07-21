# Quantum Simulation Recipes
<!-- ![Figure](./figs/idea.png) -->
[![License](https://img.shields.io/github/license/Jue-Xu/Quantum-Simulation-Recipe.svg?style=popout-square)](https://opensource.org/licenses/Apache-2.0)
[![Release](https://img.shields.io/github/v/release/jue-xu/Quantum-Simulation-Recipe?include_prereleases)](https://github.com/Jue-Xu/Quantum-Simulation-Recipe/releases)

This [python package](https://pypi.org/project/quantum-simulation-recipe/) contains ingredients for quantum simulation, such as the Hamiltonians and algorithmic primitives, mainly build on [qiskit](https://www.ibm.com/quantum/qiskit), [openfermion](https://github.com/quantumlib/OpenFermion).

##  Install
```bash
conda create --name qs python=3.10 
conda activate qs
pip install quantum-simulation-recipe
```

## Usage
```python
import quantum_simulation_recipe as qsr
from quantum_simulation_recipe import spin_ham

H = spin_ham.Nearest_Neighbour_1d(4)
H.ham
```
More details
<!-- https://github.com/Jue-Xu/Quantum-Simulation-Recipe/tree/main/tests/test.ipynb -->
https://jue-xu.github.io/Quantum-Simulation-Cookbook

## Content
### Common Hamiltonians
- Spin Lattice: nearest-neighbor, power-law, IQP
- Fermion: chemical molecule, SYK
- Boson: Hubbard
- Field: lattice gauge
- open system [todo]

### States
- entangled state: GHZ, W state
- random state (Haar random, one-design)

### Operator
- random Pauli strings
- OTOC

### Channels
- noise channel (depolarize, dephase)

### Measures 
- norm: operator, trace distance, fidelity ...
- error bound
- overlap, entanglement, entropy

### Algorithmic primitives
- Trotter-Suzuki (product formula)
- LCU
- QSP
- ITE

## Misc
Support Jax