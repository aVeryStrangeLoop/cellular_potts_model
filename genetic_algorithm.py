# Gradient descent subroutine for multistate-ising solver
import numpy as np


def GeneticAlgo(Init,Mutator,Crossover,H,ofile):
    ## Gradient descent module 

    GAheader(ofile)
    MAX_STEPS = 1E8 # Number of algorithm steps before stop
    nPop = 100 # Number of systems in a population
    ## Initialise population of states as mutations to current state 
    popStates = []
    for i in range(nPop):
        popStates.append(Mutator(Init))   

    # Calculate hamiltonian for all states in population
    H_pop = np.zeros(nPop)
    for i in range(nPop):
        H_pop[i] = H(popStates[i])
    
    cur_step = 0
    
    cur_lowest_H_state = np.zeros(Init.shape)
    cur_second_lowest_H_state = np.zeros(Init.shape)

    LOWEST_STATE = cur_lowest_H_state
    LOWEST_ENERGY = H_pop[0]

    while cur_step<MAX_STEPS:
        # Get lowest H states
        partition = np.argpartition(H_pop,2)
        cur_lowest_energy = H_pop[partition[0]]
        cur_lowest_H_state = popStates[partition[0]]
        if cur_lowest_energy < LOWEST_ENERGY:
            LOWEST_ENERGY = cur_lowest_energy
            LOWEST_STATE = cur_lowest_H_state
        #PrintState(ofile,cur_step,H_pop[partition[0]],cur_lowest_H_state)
        print(cur_step,H_pop[partition[0]])
        cur_second_lowest_H_state = popStates[partition[1]]

        # Crossover these states
        crossover1,crossover2 = Crossover(cur_lowest_H_state,cur_second_lowest_H_state)
    
        nHalfPop = nPop//2
        
        # Get index of nPop/2 largest energy states
        idx_upper = np.argpartition(H_pop, -nHalfPop)[-nHalfPop:]
        
        # Randomly add mutants of crossover 1 and crossover 2 to this high energy half population
        # And recalculate their hamiltonians
        switch = True
        for i in idx_upper:
            if switch:
                popStates[i] = Mutator(crossover1)
                H_pop[i] = H(popStates[i]) 
            else:
                popStates[i] = Mutator(crossover2)
                H_pop[i] = H(popStates[i]) 
            
            switch = not switch
        
        
        cur_step += 1 
    
    PrintState(ofile,cur_step,LOWEST_ENERGY,LOWEST_STATE)    


def GAheader(ofile):
    ofile.write("## RUNNING GENETIC OPTIMIZATION MODULE##\n")
    ofile.write("# Written by Bhaskar Kumawat (@aVeryStrangeLoop)\n")
    ofile.write("step,opt_energy,opt_state\n")

def PrintState(ofile,step,optEnergy,optState):
    ofile.write("%d,%f\n" % (step,optEnergy))
    #ofile.write("%s\n" % np.array_str(optState.flatten()))
