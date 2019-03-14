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

from Data_Analyzer_Recast import *

# loop over the list, extract best r value and masses !!!


# Select Bino or Higgsino sets
parser = argparse.ArgumentParser(description='Bino or Higgsino' )
parser.add_argument('--what',  '-W', help='Bino or Higgsino'    )

args      = parser.parse_args()
WHAT     = args.what

list_path = 'SLHA_LISTS/AdditionalExcludedNewPoints_' + WHAT + '.txt'

FILES = []
for n in open(list_path,'r').readlines():
    if '#' in n: continue
    n = n.replace('\n','')
    FILES.append(n)


# folder containing the results AND the SLHA files
SLHA_Source      = '/scratch/fambrogi/PMSSM_TGQ/' +WHAT+'_NOHIGGS_RESULTS'

RESULTS = {'Glu':[] , 'Neu':[] , 'Light_S':[] ,
           'T1':[] , 'T2':[] , 'T5':[] , 'T3GQon':[] ,
            'r':[] , 'SLHA':[] , 'T':[] , 'Best_over_tot':[]}


print 'the total number of files is: ' , len(FILES)
lim_exclusion = 1.0000000001
if not os.path.isfile('Numpys/Numpys_All/NewlyExcluded_WithWeights_' +WHAT + '.npy'):
 for name in FILES: #looping over the .py results files
    slha = SLHA_Source + '/' + name + '.slha'
    slha_name = name + '.slha'
    slhaDOTpy = SLHA_Source + '/' + name.replace('\n','') +'.slha.py'
    
    if os.path.isfile(slha):
        
      execfile(slhaDOTpy)
      Dec_Status = Check_Dec(smodelsOutput)
      
      # Extracting the rValues for the best analysis only
      if (Dec_Status == 1):
          if not Is_Res(smodelsOutput, 'ATLAS-SUSY-2013-02'): continue
          for Res in smodelsOutput['ExptRes']:
              if (Res['AnalysisID'] == 'ATLAS-SUSY-2013-02' and Res['dataType'] == 'efficiencyMap'):
                  r_tot = float(Res['r'])
                  weights = Res['TxNames weights (fb)'].keys()

                  best = max([Res['TxNames weights (fb)'][k] for k in weights ])
                  sum_weights = sum([Res['TxNames weights (fb)'][k] for k in weights])

                  ratio_best_over_tot = best/sum_weights
 
                  RESULTS['Best_over_tot'].append(ratio_best_over_tot)

                  for tx, value in Res['TxNames weights (fb)'].items():    # for name, age in dictionary.iteritems():  (for Python 2.x)
                      if best == value:
#                         print 'The best tx is', tx
                         RESULTS['T'].append(tx)

#                  print 'R tot is ', r_tot , 'the best weigth is ', best , 'the total weight is ', sum_weights , 'the ratio is: ', ratio_best_over_tot
                  if r_tot > lim_exclusion:
                    
                    Glu, Char1, Char2, Neu2, Neu , Light_S , Sbot_1, Stop_1 = Extract_Masses(slha)
                    
                    RESULTS['Glu'].append(Glu) , RESULTS['Neu'].append(Neu) , RESULTS['Light_S'].append(Light_S)
                    RESULTS['SLHA'].append(slha_name) , RESULTS['r'].append(r_tot)

 np.save('Numpys/Numpys_All/NewlyExcluded_' +WHAT , RESULTS)
