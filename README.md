# amo-coherent-control
Numerical routines for the coherent control and pulse optimization of driven, dissipative two-level atomic and molecular system using QuTip.

---

# Coherent Control and Pulse Optimization in Open Two-Level AMO System

This research repository contains numerical implementations of **Quantum Optimal Control Theory (QOCT)** applied to a driven two-level atomic system. We investigate and compare the efficiency of state preparation ($|0\rangle\rightarrow|1\rangle$) using **Gradient Ascent Pulse Engineering (GRAPE)** in a closed system versus gradient-free **BFGS optimization** under an open-system Lindblad master equation framework.

---

## Theoretical Framework & Hamiltonian

We consider a two-level system interacting with a semiclassical, linearly polarized laser field. Under the **Electric Dipole Approximation** and moving into the **Rotating Wave Approximation (RWA)** on resonance, the drift Hamiltonian vanishes ($H_0 = 0$).

The time-dependent interaction Hamiltonian is defined as:

$$H_{\text{init}}(t)=\frac{\hbar}{2}\Omega(t)\sigma_x$$

Where $\Omega(t)$ represents the time-dependent **Rabi frequency** (laser control amplitude), and $\sigma_x$ is the standard Pauli-X operator representing the dipole coupling transition.

### Dissipative Dynamics (Open Quantum System)
To model a realistic AMO laboratory emvironment subject to phase fluctuations, we evolve the density matrix $\rho(t)$ via the **Lindblad Master Equation**:

$$\frac{d\rho}{dt}=-\frac{i}{\hbar}[H_{\text{init}}(t),\rho(t)]+\mathcal{D}[\rho(t)]$$

The dissipator $\mathcal{D}[\rho(t)]$ accounting for pure dephasing at a rate $\gamma_\phi$ is given by:

$$\mathcal{D}[\rho(t)]=\gamma_\phi\left(\sigma_z\rho(t)\sigma_z-\frac{1}{2}\lbrace\sigma_z^2,\rho(t)\rbrace\right)$$

---

## Numerical Simulations & Benchmark Analysis

### 1. Unitary Control via GRAPE [(OCT.py)](OCT.py)
In the absence of environmental coupling ($\gamma_\phi=0$), we implement the GRAPE algorithm to discretize the pulse into $N=100$ constant slices over a total duration of $t_f=3.0\text{ ps}$. The system converges tightly to a target fidelity error threshold of $10^{-5}$.

**Terminal Execution Metrices**
* **Optimization Status**: Successfully Finished
* **Final Success Fidelity**: 1.00000 (Absolute state preparation saturation)
