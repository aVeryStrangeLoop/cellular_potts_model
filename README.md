# Multistate Ising Equilibrium solver

A solver to find the lowest energy state of a 2D ising like system with each cell containing any number of states. The list of accessible states, a hamiltonian and system size etc is provided by the user. The solver will then perform optimization over the system cells using the following available methods:

1. Gradient Descent (Less efficient, might not work for systems with multiple local minima, slowest. Guaranteed to converge with single global minima)
2. Simulated Annealing (Stochastic descent, prevents getting stuck in local minima to some extent, faster then next two) 
3. Evolutionary algorithm 

The output is obtained in terms of the equilibrium cell states and some thermodynamic properties of the system (like entropy and an order parameter). The program will be written in C++ to ensure fast execution.

Some references
[1] https://www.dcs.warwick.ac.uk/~englert/publications/ising_ppsn04.pdf  (Evolutionary algorithm for normal ising model)
[2] Metropolis, Nicholas, et al. "Equation of state calculations by fast computing machines." The journal of chemical physics 21.6 (1953): 1087-1092. (Metropolis algorithm)

