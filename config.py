# Part of the multistate-ising solver package written by Bhaskar Kumawat (@aVeryStrangeLoop)
# Filename : config.py
# Contains : configuration for running the solver
# Dependencies : numpy
import copy
import numpy as np
import random


class cConfig:
    ### Configuration class contains all user-define parameters required during runtime  
    ### Change the following parameters as per liking
     
    STATES = np.array([0,1]) # Possible states of the system, given as a numpy array, each state type has an idx 
    
    CONSERVED = True # If this is set to true, the mutator ensures that the total number of each state is conserved during the run
    EXCHANGE_MODE = 0 # If Conserved is true, cells can be exchanged in three ways // TODO, modes 1 and 2 not implemented yet
    # Global exchange : mode= 0 
    # Four nearest neighbor exchange : mode = 1
    # Eight nearest neighbor exchange : mode = 2 


    DEBUG_MODE = False # Set to True to get a verbose output

    WORLD_X = 50 # Cells in X direction
    WORLD_Y = 50 # Cells in y direction

    MODE = 0 # Monte-carlo mode (0 = Constant temperature, 1 = cooling)

    steps = 1000 # Total number of steps for monte_carlo(mode=0)/simulated annealing(mode=1)

    save_every = 10 # Save system state every <save_every> steps

    ## Monte-Carlo temperature (if mode==0)
    temp_constant = 20.
    
    ## Cooling properties (if mode ==1)
    temp_init = 1E20 # Initial temperature (Only applicable if mode==1)
    temp_final = 1E-20 # Final temperature (Only applicable if mode==1)

    def H(self,Z):
        # Hamiltonian calculation for a given grid Z
        # Z is a numpy array

        # Write your own code here to output the hamiltonian given a system configuration
        if self.DEBUG_MODE:
            print "Calculating hamiltonian"
        
        # Hamiltonian = summation (1 - delta(i,j,i',j'))
        h = 0.0

        X = Z.shape[0]
        Y = Z.shape[1]

        for i in range(X):
            for j in range(Y):
                h_ij = 1.0
                self_state = Z[i,j]
                #left neighbor
                if i-1>=0:
                    left_state = Z[i-1,j]
                else:
                    left_state = Z[X-1,j]
                if self_state == left_state:
                    h_ij -= 1.0
		

                # right neighbor
                if i+1<=X-1:
                    right_state = Z[i+1,j]
                else:
                    right_state = Z[0,j]
                if self_state == right_state:
                    h_ij -= 1.0

                # bottom neighbor
                if j-1>=0:
                    bot_state = Z[i,j-1]
                else:
                    bot_state = Z[i,Y-1]
                if self_state == bot_state:
                    h_ij -= 1.0

                # top neighbor
                if j+1<=Y-1:
                    top_state = Z[i,j+1]
                else:
                    top_state = Z[i,0]    
                if self_state == top_state:
                    h_ij -= 1.0
             
                h += h_ij
                

        return h/2. # Compensate for double counting
    
    def StateMutator(self,cur_state):
        # Defines how a cell's state is mutated

        # For now we assume it's chosen randomly out of the given states, but it can also be constructed from cur_state
        new_state = random.choice(self.STATES)

        while new_state==cur_state:
            new_state = random.choice(self.STATES)      

        if self.DEBUG_MODE:
            print "%d state mutated to %d" % (cur_state,new_state)
        return new_state
        

    def Mutator(self,Z):
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
            

    def InitSys(self):
        # Sets the initial configuration of the system
        # For now it is chosen randomly from given states, change this function to change the initial config
        init = np.random.choice(self.STATES,(self.WORLD_X,self.WORLD_Y))
        if self.DEBUG_MODE:
            print "Initialised configuration,"
            print init
        return init
        

    # Sanity check to make sure all elements of Z are in self.STATES, private method 
    def __SanityCheck(self,Z):
        check = np.isin(Z,self.STATES)
        return np.all(check)

