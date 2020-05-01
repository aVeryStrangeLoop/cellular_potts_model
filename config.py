# Part of the multistate-ising solver package written by Bhaskar Kumawat (@aVeryStrangeLoop)
# Filename : config.py
# Contains : configuration for running the solver
# Dependencies : numpy
import copy
import numpy as np
import random
## This class contains the main elements that can be accessed by the main program during runtime

class cConfig:
    # Define accesible states
    
    # Can be a array of any python numerical type that can be used further for calculating hamiltonian using user-defined function
    STATES = np.array([0,1]) 
    # State number conserved?
    # If this is set to true, both GA and SA ensure that the total number of each state is conserved during the run
    CONSERVED = False

    # Set this to true to get a verbose output
    DEBUG_MODE = True

    # Define world dimensions
    # Number of cells in both X and Y directions
    WORLD_X = 20
    WORLD_Y = 20

    # Define the methods to use for optimization.
    # SA = Simulated Annealing, GA = Genetic Algorithm
    METHODS = ["SA"] 

    # Define hamiltonian
    ## NOTE : You might have to write accessory functions if you want to implement complex hamiltonians. For eg - period boundaries will require functions to calculate interactions across boundaries.
    def H(self,Z):
        # Z is a numpy array
        # Write your own code here to output the hamiltonian given a system configuration
        if self.DEBUG_MODE:
            print "Calculating hamiltonian"
        h = np.sum(Z)
        return h
    
    def StateMutator(self,cur_state):
        # Defines how a cell's state is mutated

        # For now we assume it's chosen randomly out of the given states, but it can also be constructed from cur_state
        new_state = random.choice(self.STATES)

        while new_state==cur_state:
            new_state = random.choice(self.STATES)      

        if self.DEBUG_MODE:
            print "%d state mutated to %d" % (cur_state,new_state)
        return new_state
        

    def SAMutator(self,Z):
        ## If conserved status is false, mutate only one cell
        if not self.CONSERVED:
            # Give the system state derived after a monte-carlo step from Z
            # Coordinate of random cell
            i = random.randrange(0,Z.shape[0])
            j = random.randrange(0,Z.shape[1])
            # Choose any cell in Z and change its contents randomly to one of the states
            target_state = self.StateMutator(Z[i,j]) 
            if self.DEBUG_MODE:
                print "Conserved state mode OFF, randomly switching the cell state at (%d,%d) from %d to %d" % (i,j,Z[i,j],target_state)
            mut = np.copy(Z)
            mut[i,j] = target_state
            return mut

        ## If conserved status is true, swap two cells instead of just mutating one:
        elif self.CONSERVED:
            states_exchanged = False # This variable just makes sure we don't select the same cell index to exchange
            while not states_exchanged:             
                i1 = random.randrange(0,Z.shape[0])
                j1 = random.randrange(0,Z.shape[1])
            
                i2 = random.randrange(0,Z.shape[0])
                j2 = random.randrange(0,Z.shape[1])
                
                if not (Z[i1,j1]==Z[i2,j2]):
                    states_exchanged == True
                    state_1 = Z[i1,j1]
                    state_2 = Z[i2,j2]
                    
                    mut = np.copy(Z)
                    mut[i1,j1] = state_2
                    mut[i2,j2] = state_1

                    if self.DEBUG_MODE:
                        print "Conserved state mode ON, exchanging states %d and %d at (%d,%d) and (%d,%d) resp." % (state_1,state_2,i1,j1,i2,j2)
                    return mut
            
    
    def GAMutator(self,Z):
        # Mutates a state with mutation frequency freq for Genetic Algorithm
        FREQ = 0.2 ### TRY CHANGING THIS FOR BETTER RESULTS
        # Create a mask to randomly mutate array elements
        mask = np.random.choice([True,False],Z.shape,p=[FREQ,1-FREQ])
        r = np.random.choice(self.STATES,Z.shape)
        mut = Z
        mut[mask]=r[mask]
        return mut

    def GACrossover(self,State1,State2):
        # Recombines two states for Genetic algorithm
        state1_flat = State1.flatten()
        state2_flat = State2.flatten()

        if State1.shape!=State2.shape:
            print("Error : In GARecombine, system state shapes not equal!")
            exit(1)
        
        nCROSSOVER = 10 #No. of crossovers

        ## CROSSOVER ALGORITHM
        ## 1. Determine indexes of nCROSSOVER points
        idx_crossover = np.random.choice(len(state1_flat),nCROSSOVER,replace=False)
        
        for idx in idx_crossover:
            tmp = state2_flat[:idx].copy()
            state2_flat[:idx], state1_flat[:idx]  = state1_flat[:idx], tmp
        
        return np.reshape(state1_flat,State1.shape),np.reshape(state2_flat,State2.shape)

    def InitConfig(self):
        # Sets the initial configuration of the system
        # For now it is chosen randomly from given states, change this function to change the initial config
        init = np.random.choice([1],(self.WORLD_X,self.WORLD_Y))
        if self.DEBUG_MODE:
            print "Initialised configuration,"
            print init
        return init
        

    # Sanity check to make sure all elements of Z are in self.STATES, private method 
    def __SanityCheck(self,Z):
        check = np.isin(Z,self.STATES)
        return np.all(check)

