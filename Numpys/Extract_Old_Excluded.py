import os,sys
import pyslha2 as pyslha
import argparse
from Data_Analyzer_Recast import *
import numpy as np

"""
 Select BINO or HIGGSINO dataset
 Usage: python Create_Numpys.py -W BINO    ( or -W HIGGSINO)
"""
parser = argparse.ArgumentParser(description='Bino or Higgsino' )
parser.add_argument('--what',  '-W', help='Bino or Higgsino'    )

args      = parser.parse_args()
WHAT     = args.what

# folder containing the results AND the SLHA files
SLHA_Source      = '/scratch/fambrogi/PMSSM_TGQ/' +WHAT+'_NOHIGGS_RESULTS'

lista = open('/scratch/fambrogi/PMSSM_TGQ/GitHub_Repo/pMSSM_TGQ/TGQ_old/'+WHAT+'_old_excluded.txt' ).readlines()

FILES = []
for line in lista:
    if '#' in line: continue
    slha = line.split(' ')[0].replace('\n','')
    FILES.append(slha)

Old     = { 'r':[] , 'Glu':[] , 'Neu':[], 'SLHA':[] , 'Light_S':[] , 'INFO': 'Blah Blah' } # I cant save arrays to a numpy dictionary!
      

for name in FILES: #looping over the .py results files
    slha = SLHA_Source + '/' + name + '.slha'

    if os.path.isfile(slha):
                  
          Glu, Char1, Char2, Neu2, Neu , Light_S , Sbot_1, Stop_1 = Extract_Masses(slha)

          Old['Glu'].append(Glu)
          Old['Neu'].append(Neu)
          Old['Light_S'].append(Light_S)
          Old['SLHA'].append(name)
          

np.save('Old_Excluded_'+WHAT , Old)
