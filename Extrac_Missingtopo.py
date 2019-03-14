import os,sys
import matplotlib
matplotlib.use('Agg')
from matplotlib  import cm
from itertools import izip
from matplotlib import ticker
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import argparse
import numpy as np

import operator

from Data_Analyzer_Recast import *


parser = argparse.ArgumentParser(description='Bino or Higgsino' )
parser.add_argument('--what',  '-W', help='Bino or Higgsino'    )

args      = parser.parse_args()
WHAT     = args.what

# folder containing the results AND the SLHA files
SLHA_Source      = '/scratch/fambrogi/PMSSM_TGQ/' +WHAT+'_NOHIGGS_RESULTS'

dire = '/scratch/fambrogi/PMSSM_TGQ/GitHub_Repo/pMSSM_TGQ/SLHA_LISTS/Still_Unexcluded_' + WHAT + '.txt'
LISTA = [ na.replace('\n','') for na in open(dire,'r').readlines() if '#' not in na] 

"""
{'weight (fb)': 70.020485798206593, 'sqrts (TeV)': 13.0, 'element': '[[[b],[b]],[[jet]]]'}, {'weight (fb)': 12.373967872399998, 'sqrts (TeV)': 13.0, 'element': '[[[b]],[[jet]]]'}
"""


def Extract_Masses(slha):
    
    readfile = pyslha.readSLHAFile(slha)
    Glu   = readfile[0]['MASS'].entries[1000021]
    Char1 = readfile[0]['MASS'].entries[1000024]
    Char2 = readfile[0]['MASS'].entries[1000037]
    Neu = abs(readfile[0]['MASS'].entries[1000022])
    Neu2 = readfile[0]['MASS'].entries[1000023]
    
    eL, muL, eR, muR = readfile[0]['MASS'].entries[1000011],readfile[0]['MASS'].entries[1000013],readfile[0]['MASS'].entries[2000011],readfile[0]['MASS'].entries[2000013]
    
    Sbot_1 = readfile[0]['MASS'].entries[1000005]
    Stop_1 = readfile[0]['MASS'].entries[1000006]
    # ul=dl=cl=sl , ur=cr , dr=sr [valid for the pMSSM(19)]
    Sq_L   = readfile[0]['MASS'].entries[1000001]
    Sq_U_R = readfile[0]['MASS'].entries[2000002]
    Sq_D_R = readfile[0]['MASS'].entries[2000001]
    
    Light_S = min(Sq_L , Sq_U_R , Sq_D_R)
    
    return Glu, Char1, Char2, Neu2, Neu , Light_S , Sbot_1, Stop_1


def Extract_BestMissingTopo(smodelsOutput,SLHA = ''):
    """ Extract the best missing topo and its weight """
    miss = smodelsOutput['Missed Topologies']
    elem , w = miss[0]['element'], miss[0]['weight (fb)']
    return elem, w



missing_topo = []
weights = []
slha = []
Glu, Sq, Neu = [], [] ,[]
""" I loop over the slha and extract the best missing topo, its weight and slha name (for later extracting the masses """
for s in LISTA:
   py = SLHA_Source + '/' + s + '.slha.py' # path tp the .py files                                                                                                                                         
   execfile(py)
   t,w = Extract_BestMissingTopo(smodelsOutput,SLHA = s)
   missing_topo.append(t), weights.append(w) , slha.append(s)
   glu, Char1, Char2, Neu2, neu , light_S , Sbot_1, Stop_1 = Extract_Masses(SLHA_Source + '/' + s + '.slha')                         
   Glu.append(glu) , Neu.append(neu) , Sq.append(light_S) 

comm ='Containes the best missing topo for the non excluded points after the addition of TGQ maps'

Results = {'Topo': missing_topo , 'w': weights , 'slha': slha , 'Glu': Glu , 'Light_Sq': Sq , 'Neu': Neu , 'C': comm , 'Sorted':''}


Unique_Missing = list(set(missing_topo))

print 'Different Missing topo: ' , Unique_Missing  , len(Unique_Missing) 

# I create a dictionary where key = misisng topo , value = frequency
Topo_Dic = {}
for diff in Unique_Missing:
    print diff , ' ' , missing_topo.count(diff) # I count the occurrence of the misisng topo in the total list
    Topo_Dic[diff] = missing_topo.count(diff)

sorted_topo = sorted(Topo_Dic.items(), key=operator.itemgetter(1) , reverse = True)
print 'Sorted missing topologies: ', sorted_topo

Results['Sorted'] = sorted_topo


# Saving all in the numpy dic
np.save('Numpys/Numpys_All/Missing_Topologies_'     + WHAT , Results )
