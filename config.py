# Part of the multistate-ising solver package written by Bhaskar Kumawat (@aVeryStrangeLoop)
# Filename : config.py
# Contains : configuration for running the solver
# Dependencies : numpy
import copy
import numpy as np
import random
import math

class cConfig:
    ### Configuration class contains all user-define parameters required during runtime  
    ### Change the following parameters as per liking
     
    TYPES = np.array([0,1,2]) # Possible states of the system, given as a numpy array, each state type has an idx 
    ### Light = 0 , Dark = 1, Medium = 2
    # Number of cells of each type    
    TOTAL_SPINS = 100 # Number of cells/spins
    SPINS = np.array(range(TOTAL_SPINS))# Each grid-cell has a spin from this set 

    DEBUG_MODE = False # Set to True to get a verbose output


    # MAKE SURE YOU HAVE ENOUGH CELLS TO ACCOMODATE THE MAX TARGET AREA * TOTAL_SPINS limit
    WORLD_X = 100 # Cells in X direction
    WORLD_Y = 100 # Cells in y direction

    MODE = 0 # Monte-carlo mode (0 = Constant temperature, 1 = cooling)

    MAX_MCS = 400

    steps = MAX_MCS*16.*TOTAL_SPINS # Total number of steps for monte_carlo(mode=0)/simulated annealing(mode=1)

    save_every = 100 # Save system state every <save_every> steps

    ## Monte-Carlo temperature (if mode==0)
    temp_constant = 1.0
    
    ## Cooling properties (if mode ==1)
    temp_init = 1000.0 # Initial temperature (Only applicable if mode==1)
    temp_final = 0.1 # Final temperature (Only applicable if mode==1)

    def H(self,state):
        # Hamiltonian calculation for a given grid state
        spins = state[0]
        spin_types = state[1]
        # Write your own code here to output the hamiltonian given a system configuration
        if self.DEBUG_MODE:
            print "Calculating hamiltonian"
        
        # Parameters for glazier model
        def J(s1,s2):
            J00 = 14. # Surface energy between 0-0 (light-light)
            J11 = 2. # Surface energy between 1-1 (dark-dark)
            J22 = 0. # Surface energy between 2-2 (med-med)


            J01 = 11. # Surface energy between 0-1 (light-dark)
        
            J12 = 16. # Surface energy between 1-2 (dark-medium)
            J02 = 16. # Surface energy between 0-2 (light-medium)
            
            if (s1==0 and s2==0):
                return J00
            elif (s1==1 and s2==1):
                return J11
            elif (s1==2 and s2==2):
                return J22
            elif (s1==0 and s2==1) or (s1==1 and s2==0):
                return J01
            elif (s1==1 and s2==2) or (s1==2 and s2==1):
                return J12
            elif (s1==0 and s2==2) or (s1==2 and s2==0):
                return J02

        lambda_area = 1. # Strength of area constraint

        target_areas = [40.,40.,-1] # Target area for the three cell types (light,dark,med)

        def theta(target_area):
            if target_area > 0:
                return 1.
            elif target_area < 0 :
                return 0.
        
        def delta(t1,t2): # Delta function
            if t1==t2:
                return 1.
            else:
                return 0.

        h = 0.0

        X = spins.shape[0]
        Y = spins.shape[1]

        spin_areas = np.zeros(self.TOTAL_SPINS) # Areas of all cells

        # Add interaction energies (and count area of each state)
        for i in range(X):
            for j in range(Y):
                self_spin = spins[i,j]
                self_type = spin_types[self_spin]
                spin_areas[self_spin]+=1 # add to total area of this spin
                neighbor_spins = []
                ## REMOVED PERIODIC BOUNDARIES
                #left neighbor
                #neighbor_spins.append(spins[i-1,j] if i-1>=0 else spins[X-1,j])
                if i-1>=0:
                    neighbor_spins.append(spins[i-1,j])
                # right neighbor
                #neighbor_spins.append(spins[i+1,j] if i+1<=X-1 else spins[0,j])
                if i+1<=X-1:
                    neighbor_spins.append(spins[i+1,j])
                # bottom neighbor
                #neighbor_spins.append(spins[i,j-1] if j-1>=0 else spins[i,Y-1])
                if j-1>=0:
                    neighbor_spins.append(spins[i,j-1])
                # top neighbor
                #neighbor_spins.append(spins[i,j+1] if j+1<=Y-1 else spins[i,0])
                if j+1<=Y-1:
                    neighbor_spins.append(spins[i,j+1])

                for i in range(len(neighbor_spins)): 
                    h += J(spin_types[self_spin],spin_types[neighbor_spins[i]])*(1.-delta(self_spin,neighbor_spins[i]))

        h = h/2. # compensate for double counting of neighbor pairs
                
        # Add area constraint energies
        for i in range(self.TOTAL_SPINS): # For each spin 
            a = spin_areas[i]
            A = target_areas[spin_types[i]] # Target area for the type for this spin
            h += lambda_area * theta(A) * (a-A) * (a-A)


        return h
     

    def Mutator(self,state):
        ## If conserved status is false, mutate only one cell
        spins = state[0]
        spin_types = state[1]

        i1 = -1
        i2 = -1
        j1 = -1
        j2 = -1

        spin1 = -1
        spin2 = -1
        while spin1==spin2:
            # Choose a random cell and change its spin to spin of one of its neighbors given these two spins are not the same
            i1 = random.randrange(0,spins.shape[0])
            j1 = random.randrange(0,spins.shape[1])
            spin1 = spins[i1,j1]
            neighbor_chosen = False
 	
            while not neighbor_chosen:           
                randir = random.choice([[0,1],[1,0],[0,-1],[-1,0]])
	
                i2 = i1 + randir[0]
                j2 = j1 + randir[1]

                if not (i2>=spins.shape[0] or i2<0 or j2>=spins.shape[1] or j2<0): 
                    neighbor_chosen = True
            spin_2 = spins[i2,j2]
                    
        mut = np.copy(spins)
        mut[i1,j1] = spin_2
        if self.DEBUG_MODE:
            print "Flipping spin %d to %d at (%d,%d) and (%d,%d) resp." % (state_1,state_2,i1,j1,i2,j2)
        return [mut,spin_types]
            

    def InitSys(self):
        # Sets the initial configuration of the system
        # Randomly from given types and spins. State of the system is defined by the list [types,spins]
        init_spins = np.random.choice(self.SPINS,(self.WORLD_X,self.WORLD_Y))
        spin_types = np.random.choice(self.TYPES,(self.TOTAL_SPINS)) # This array contains the type associated with each spin
        # spin_types[i] = type associated with spin no. i
        if self.DEBUG_MODE:
            print "Initialised configuration,"
            print init_types
            print init_spins
        return [init_spins,spin_types]
        

    def SpinsToTypes(self,state):
        spins = state[0]
        spin_types = state[1]
        types = np.zeros(spins.shape)
        for i in range(spins.shape[0]):
            for j in range(spins.shape[1]):
                types[i,j] = spin_types[spins[i,j]]
        return types
