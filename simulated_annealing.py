# Simulated Annealing subroutine for multistate-ising solver
import numpy as np
import random

def Cooling(time):
    T_init = 10.
    tau = 1000000.
    return T_init*np.exp(-time/tau)
	
def SimulatedAnneal(InitSys,Mutator,H,ofile):
    
    SAheader(ofile)

    STEPS = 100000000

	
    optState = InitSys # Stores the most optimal state ever encountered
    optEnergy = H(InitSys)
 
    curState = InitSys # Stores the current state
    curEnergy = H(InitSys)
	
    cur_step = 0

    while STEPS > cur_step:
		
        T_cur = Cooling(float(cur_step)) 

        PrintAnnealState(ofile,T_cur,curEnergy,optEnergy)
        print(T_cur,curEnergy,optEnergy)

        accepted = False
        
        
        neighborState = Mutator(curState)
        neighborEnergy = H(neighborState)
            
        isaccepted = ToAccept(curEnergy,neighborEnergy,T_cur)
            
        if isaccepted:
            curState = neighborState
            curEnergy = neighborEnergy
        
        if curEnergy < optEnergy:
            optState = curState
            optEnergy = curEnergy


        cur_step += 1

    ofile.write("# END OF SIMULATED ANNEALING")
    np.savetxt(optState,"optimal_state.csv")

def ToAccept(E_cur,E_new,T): # Acceptance probability
    if E_new < E_cur:
        return True
    else:
        delta = E_new-E_cur
        prob =  np.exp(-delta/T)
        if prob>random.random():
            return True
        else:
            return False


def SAheader(ofile):
    ofile.write("## RUNNING SIMULATED ANNEALING MODULE##\n")
    ofile.write("# Written by Bhaskar Kumawat (@aVeryStrangeLoop)\n")
    ofile.write("T,cur_energy,opt_energy\n")

def PrintAnnealState(ofile,T,cur_energy,opt_energy):
    ofile.write("%d,%f,%f\n" % (T,cur_energy,opt_energy))
    #ofile.write("%s\n" % np.array_str(cur_state.flatten()))
