import os,sys
import matplotlib
matplotlib.use('Agg')
from matplotlib  import cm
from itertools import izip
from matplotlib import ticker
#from Plotter_Functions import *
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import argparse
import numpy as np
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
from Data_Analyzer_Recast import Check_Dec
import pyslha2 as pyslha
from Functions import *


# Select Bino or Higgsino sets
parser = argparse.ArgumentParser(description='Bino or Higgsino' )
parser.add_argument('--what',  '-W', help='Bino or Higgsino'    )

args      = parser.parse_args()
WHAT     = args.what

SLHA_Source = '/scratch/fambrogi/PMSSM_TGQ/'+WHAT+'_NOHIGGS_RESULTS/'


FILES = []
for name in os.listdir(SLHA_Source):
    if '.slha' in name and '.smodels' not in name and '.py' not in name:
         NAME = name
         if os.path.isfile(SLHA_Source +'/'+ NAME + '.smodels') and  os.path.isfile(SLHA_Source + '/'+ NAME + '.py'):
              FILES.append(NAME + '.py')

#FILES = [ name for name in os.listdir(SLHA_Source) if '.slha.py' in name and os.path.isfile()] # All results in .py files


print 'the total number of files is: ' , len(FILES)


def Extract_rValue_txName(Res, txName = ''):
            r = [0]
            for key in Res['TxNames weights (fb)'].keys():
                if key == txName:
                    r.append(Res['TxNames weights (fb)'][txName] / Res['upper limit (fb)'])
            return max(r)

def Is_Res(smodelsOutput, ANALYSIS):
    Is_Result = False
    for Res in smodelsOutput['ExptRes']:
        if (Res['AnalysisID'] == ANALYSIS):
            Is_Result = True
    return Is_Result



lim_exclusion = 1.00001
not_exc = []
RESULTS = {'Glu':[] , 'Neu':[] , 'Light_S':[] ,
           'T1':[] , 'T2':[] , 'T5':[] , 'T3GQon':[] ,
            'r':[] , 'SLHA':[] }
print 'the total number of files is: ' , len(FILES)
for name in FILES: #looping over the .py results files
    slha_name = name.replace('.py','').replace('\n','')
    slha = SLHA_Source + '/' + slha_name
    slhaDOTpy = SLHA_Source + '/' + name.replace('\n','')
    
    if os.path.isfile(slha):
        
      execfile(slhaDOTpy)
      Dec_Status = Check_Dec(smodelsOutput)
      
      # Extracting the rValues for the best analysis only
      if (Dec_Status == 1):
          if not Is_Res(smodelsOutput, 'ATLAS-SUSY-2013-02'): continue
          for Res in smodelsOutput['ExptRes']:
              if (Res['AnalysisID'] == 'ATLAS-SUSY-2013-02' and Res['dataType'] == 'efficiencyMap'):
                  r_tot = float(Res['r'])
                  if r_tot > lim_exclusion:
                    T1  = Extract_rValue_txName(Res, txName = 'T1')
                    T2  = Extract_rValue_txName(Res, txName = 'T2')
                    T5  = Extract_rValue_txName(Res, txName = 'T5')
                    TGQ = Extract_rValue_txName(Res, txName = 'T3GQon')
                    
                    Glu, Char1, Char2, Neu2, Neu , Light_S , Sbot_1, Stop_1 = Extract_Masses(slha)
                    
                    RESULTS['Glu'].append(Glu) , RESULTS['Neu'].append(Neu) , RESULTS['Light_S'].append(Light_S) , RESULTS['SLHA'].append(slha_name)
                    RESULTS['T1'].append(T1), RESULTS['T2'].append(T2) , RESULTS['T5'].append(T5) , RESULTS['T3GQon'].append(TGQ) , RESULTS['r'].append(r_tot)


print str(len(RESULTS['Glu']))

#print r_tot , T1, T2 , T5 , TGQ , T1+T2+T5+TGQ

np.save('Numpys_All/ATLAS02_Excluded_'     + WHAT , RESULTS )

