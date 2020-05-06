# Main file to run the multistate-ising optimization routine
# Written by Bhaskar Kumawat for PH354 as a part of the multistate-ising package

from config import cConfig
from simulated_annealing import SimulatedAnneal
import sys
import datetime 
import numpy as np

def main(args):
    # Get configuration from the cConfig.py file
    conf = cConfig()

    # Start an output file where all the results will be stored
    ofile = open("results.csv","w+")
    WriteHeader(ofile,conf)
    
    InitSys = conf.InitConfig()

    ############################### RUN Simulated Annealing
    # Inputs:
    # 1. Initial State of the system
    # 2. Mutator that gives a random neighbor in the surrounding
    # 3. Hamiltonian to minimize
    # 4. Output file where the algorithm writes results
    ###############################
    
    SimulatedAnneal(InitSys,conf.SAMutator,conf.H,ofile)




################################## ACCESORY FUNCTIONS
## FUNCTION TO WRITE OUTPUT FILE HEADER
def WriteHeader(ofile,conf):
    ofile.write("OUTPUT FILE FOR MULTISTATE-ISING SOLVER \n")
    ofile.write("Written by Bhaskar Kumawat (github.com/aVeryStrangeLoop)\n")

    ofile.write("RUN STARTED AT,"+str(datetime.datetime.now())+"\n")

    ofile.write("WORLD_X,%d\n" % conf.WORLD_X)
    ofile.write("WORLD_Y,%d\n" % conf.WORLD_Y)
    ofile.write("##################### START OF OPTIMIZER OUTPUTS ###################\n")

if __name__=="__main__":
    main(sys.argv)


