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
           'T1':[] , 'T2':[] , 'T5':[] , 'T3GQ':[] ,
            'r':[] , 'SLHA':[] , 'W':[]}
print 'the total number of files is: ' , len(FILES)
lim_exclusion = 1.0000000001
"""
{'TxNames': ['T2', 'T3GQon', 'T5'], 'AnalysisSqrts (TeV)': 8.0, 'r_expected': 9.3306448421758894, 'maxcond': 0.0, 'chi2': 25.506795027456672, 'Mass (GeV)': None, 'upper limit (fb)': 1.8181, 'TxNames weights (fb)': {'T5': 1.7540826715440161, 'T2': 0.85033375312882642, 'T3GQon': 11.507250834633972}, 'theory prediction (fb)': 14.111667259306813, 'lumi (fb-1)': 20.300000000000001, 'dataType': 'efficiencyMap', 'expected upper limit (fb)': 1.5124, 'r': 7.7617662721009921, 'likelihood': 3.9391545965235421e-09, 'DataSetID': 'SR2jt', 'AnalysisID': 'ATLAS-SUSY-2013-02'}
"""


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
                  TX =  Res['TxNames']
                  tot_weight = Res['theory prediction (fb)']
                  RESULTS['W'].append(tot_weight)
                  if 'T2' in TX:
                      RESULTS['T2'].append(Res['TxNames weights (fb)']['T2'])
                  else: RESULTS['T2'].append(-1)
                  if 'T5' in TX:
                            RESULTS['T5'].append(Res['TxNames weights (fb)']['T5'])
                  else: RESULTS['T5'].append(-1)
                  if 'T3GQon' in TX:
                            RESULTS['T3GQ'].append(Res['TxNames weights (fb)']['T3GQon'])
                  else:RESULTS['T3GQ'].append(-1)
                  if 'T1' in TX:
                            RESULTS['T1'].append(Res['TxNames weights (fb)']['T1'])
                  else: RESULTS['T1'].append(-1)

                  
                  r_tot = float(Res['r'])
                  if r_tot > lim_exclusion:
                    
                    Glu, Char1, Char2, Neu2, Neu , Light_S , Sbot_1, Stop_1 = Extract_Masses(slha)
                    
                    RESULTS['Glu'].append(Glu) , RESULTS['Neu'].append(Neu) , RESULTS['Light_S'].append(Light_S)
                    RESULTS['SLHA'].append(slha_name) , RESULTS['r'].append(r_tot)

np.save('Numpys/Numpys_All/Weights_NewlyExcluded_' +WHAT , RESULTS)

