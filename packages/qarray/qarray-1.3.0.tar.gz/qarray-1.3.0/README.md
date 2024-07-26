

![PyPI](https://img.shields.io/pypi/v/qarray)
[![arXiv](https://img.shields.io/badge/arXiv-2404.04994-Green.svg)](https://arxiv.org/abs/2404.04994)
[![Read the Docs](https://img.shields.io/readthedocs/qarray)](https://qarray.readthedocs.io/en/latest/introduction.html)
![GitHub Workflow Status](https://github.com/b-vanstraaten/qarray/actions/workflows/windows_tests.yaml//badge.svg)
![GitHub Workflow Status](https://github.com/b-vanstraaten/qarray/actions/workflows/macos_tests.yaml//badge.svg)
![GitHub Workflow Status](https://github.com/b-vanstraaten/qarray/actions/workflows/linux_tests.yaml//badge.svg)

# QArray

Paper: [QArray: a GPU-accelerated constant capacitance model simulator for large quantum dot arrays; Barnaby van Straaten, Joseph Hickie, Lucas Schorling, Jonas Schuff, Federico Fedele, Natalia Ares](https://arxiv.org/abs/2404.04994)

Documentation:[https://qarray.readthedocs.io/en/latest/introduction.html](https://qarray.readthedocs.io/en/latest/introduction.html)

<p align="center">
    <img src="https://github.com/b-vanstraaten/qarray/blob/main/docs/source/figures/GUI.jpg" alt="structure" width="800">
</p>

**QArray** harnesses the speed of the systems programming language Rust or the compute power of GPUs using JAX XLA to
deliver constant capacitance model charge stability diagrams in seconds or milliseconds. It couples highly optimised and
parallelised code with two new algorithms to compute the ground state charge configuration. These algorithms scale
better than the traditional brute-force approach and do not require the user to specify
the maximum number of charge carriers a priori. QArray includes a graphical user interface (GUI) that allows users to
interact with the simulation in real-time.

<p align="center">
<img src="https://github.com/b-vanstraaten/qarray/blob/main/docs/source/figures/structure.jpg" alt="structure" width="400">
</p>

QArray runs on both CPUs and GPUs and is designed to be easy to use and integrate into your existing workflow. It was
developed on macOS running on Apple Silicon and is continuously tested on Windows-lastest, macOs13, macOS14 and
Ubuntu-latest.

Finally, QArray captures physical effects such as measuring the charge stability diagram with a SET and thermal
broadening of charge transitions. The combination of these effects permits the simulation of charge stability diagrams
that are visually similar to those measured experimentally. The plots on the right below are measured experimentally,
and the plots on the left are simulated using QArray.

<p align="center">
<img src="https://github.com/b-vanstraaten/qarray/blob/main/docs/source/figures/structure.jpg" alt="structure" width="400">
</p>

Figure (a) shows the charge stability diagram of an open quadruple quantum dot array recreated with permission
from [[1]](#[1]) while (b) is a simulated using QArray.

Figure (c) shows the charge stability diagram of a closed five dot quantum recreated with permission from  [[2]](#[2])
and (d) is
simulated using QArray.

## Installation

We have tried to precompile the binaries for as many platforms as possible if you are running one of those operating
systems, you can install QArray with just pip:
```bash
pip install qarray
```

If you slip through the gaps, then the pip install will try to compile the binaries for you. This might require you to
install some additional dependencies. In particular, might need to have cmake and rust installed.

Install Rust from:
[https://www.rust-lang.org/tools/install](https://www.rust-lang.org/tools/install)

Install CMake from:
[https://cmake.org/download/](https://cmake.org/download/)
however, on macOS and Ubuntu, you can install cmake using homebrew and apt, respectively.

Also, setting up JAX on macOS running on M series chips can be a bit finicky. We outline the steps that worked for us
in [macOS installation](#macOS-installation). Alternatively, just spin up
a [Github Codespace](https://github.com/codespaces), then ```pip install qarray``` and
you are done.

## Getting started - double quantum dot example

```python
import matplotlib.pyplot as plt
import numpy as np

from qarray import DotArray, GateVoltageComposer, charge_state_contrast

# Create a quantum dot with 2 gates, specifying the capacitance matrices in their maxwell form.

model = DotArray(
    cdd=np.array([
        [1.2, -0.1],
        [-0.1, 1.2]
    ]),
    cgd=np.array([
        [1., 0.1],
        [0.1, 1]
    ]),
    algorithm='default', implementation='rust',
    charge_carrier='h', T=0.,
)

# a helper class designed to make it easy to create gate voltage arrays for nd sweeps
voltage_composer = GateVoltageComposer(n_gate=model.n_gate)

# defining the min and max values for the dot voltage sweep
# defining the min and max values for the dot voltage sweep
vx_min, vx_max = -5, 5
vy_min, vy_max = -5, 5
# using the dot voltage composer to create the dot voltage array for the 2d sweep
vg = voltage_composer._do2d(0, vy_min, vx_max, 400, 1, vy_min, vy_max, 400)

# run the simulation with the quantum dot array open such that the number of charge carriers is not fixed
n_open = model.ground_state_open(vg)  # n_open is a (100, 100, 2) array encoding the
# number of charge carriers in each dot for each gate voltage
# run the simulation with the quantum dot array closed such that the number of charge carriers is fixed to 2
n_closed = model.ground_state_closed(vg, n_charges=2)  # n_closed is a (100, 100, 2) array encoding the
# number of charge carriers in each dot for each gate voltage


charge_state_contrast_array = [0.8, 1.2]

# creating arrays that encode when the dot occupation changes
z_open = charge_state_contrast(n_open, charge_state_contrast_array)
z_closed = charge_state_contrast(n_closed, charge_state_contrast_array)

# plot the results
fig, ax = plt.subplots(1, 2, figsize=(10, 5))
ax[0].imshow(z_open.T, extent=(vx_min, vx_max, vy_min, vy_max), origin='lower', cmap='binary')
ax[0].set_title('Open Dot Array')
ax[0].set_xlabel('Vx')
ax[0].set_ylabel('Vy')
ax[1].imshow(z_closed.T, extent=(vx_min, vx_max, vy_min, vy_max), origin='lower', cmap='binary')
ax[1].set_title('Closed Dot Array')
ax[1].set_xlabel('Vx')
ax[1].set_ylabel('Vy')
plt.tight_layout()
plt.show()
```
## Examples

The examples folder contains a number of examples that demonstrate how to use the package to simulate different quantum
dot systems.

1. [Double Quantum Dot](https://github.com/b-vanstraaten/qarray/blob/main/examples/double_dot.ipynb)
2. [Linear Triple Quantum Dot](https://github.com/b-vanstraaten/qarray/blob/main/examples/triple_dot.ipynb)
3. [Linear Quadruple Quantum Dot](https://github.com/b-vanstraaten/qarray/blob/main/examples/quadruple_dot.ipynb)
4. [Charge sensed double quantum dot](https://github.com/b-vanstraaten/qarray/blob/main/examples/charge_sensing.py)

## References

<a name="[1]"></a>
[1] [Full control of quadruple quantum dot circuit charge states in the single electron regime](https://pubs.aip.org/aip/apl/article/104/18/183111/24127/Full-control-of-quadruple-quantum-dot-circuit)

<a name="[2]"></a>
[2] [Coherent control of individual electron spins in a two-dimensional quantum dot array](https://www.nature.com/articles/s41565-020-00816-w)

## macOS installation

Getting JAX to work macOS on M Series chips can be rather finicky. Here are the steps we used to get everything working
starting from a fresh OS install.

1. Install homebrew from https://brew.sh and run through the install script

2. Use homebrew to install miniconda

```zsh
brew install  miniconda
```

3. Use homebrew to install cmake

```zsh
brew install cmake
```

4. Create a new conda environment and install pip

```zsh
conda create -n qarray python=3.10
conda activate qarray
conda install pip
```

5. Install qarray using pip

```zsh
pip install qarray
```

This installation script has been demonstrated to work on macOS Ventura 13.4 and Sonoma 14.4.
To install directly from the repository, use the command:
```zsh
pip install git+https://github.com/b-vanstraaten/qarray.git@main
```

