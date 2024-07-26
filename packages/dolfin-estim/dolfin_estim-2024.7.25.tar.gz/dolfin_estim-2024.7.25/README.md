# dolfin_estim


### Installation

A working installation of [FEniCS](https://fenicsproject.org) (version 2019.1.0) is required to run `dolfin_estim`.
To setup a system, the simplest is to use [conda](https://conda.io): first install [miniconda](https://docs.conda.io/projects/miniconda/en/latest) (note that for Microsoft Windows machines you first need to install WSL, the [Windows Subsystem for Linux](https://learn.microsoft.com/en-us/windows/wsl/install), and then install miniconda for linux inside the WSL; for Apple MacOS machines with Apple Silicon CPUs, you still need to install the MacOS Intel x86_64 version of miniconda), and then install the necessary packages:
```
conda create -y -c conda-forge -n dolfin_estim fenics=2019.1.0 meshio=5.3 mpi4py=3.1.3 pip python=3.10
conda activate dolfin_estim
pip install dolfin_estim numpy==1.24
```