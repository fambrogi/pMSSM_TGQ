import os,sys
import pyslha2 as pyslha
import argparse
from Data_Analyzer_Recast import *
import numpy as np

"""
 Select BINO or HIGGSINO dataset
 Usage: python Create_Numpys.py -W BINO    ( or -W HIGGSINO)
 This creates the dictionary from the list of OLD excluded points, and from the TOTAL POINTS exlcuded by ATLAS official paper
"""
parser = argparse.ArgumentParser(description='Bino or Higgsino' )
parser.add_argument('--what',  '-W', help='Bino or Higgsino'    )
args      = parser.parse_args()
WHAT     = args.what
LISTA = WHAT

# folder containing the results AND the SLHA files
folder = '/scratch/fambrogi/PMSSM_TGQ/'+WHAT+'_NOHIGGS_RESULTS/'

'''
##### OLD EXCLUDED POINTS
# Extract the data for the OLD excluded points
old_list = '/scratch/fambrogi/PMSSM_TGQ/GitHub_Repo/pMSSM_TGQ/SLHA_LISTS/' + WHAT + '_old_excluded.txt'
lista = open(old_list,'r').readlines()[1:]

print '*** The total number of files excluded by OLD SModels Publication is: ' , len(lista)
print '\n*** Creating the numpys files containing the dictionaries \n ***'

Masses = {'SLHA':[] , 'Glu':[] , 'Neu':[] , 'Light_S':[] }
for slha in lista:
    slha = slha.replace('\n','')
    #print slha 
    slha_path = folder + slha + '.slha'

    Glu, Char1, Char2, Neu2, Neu , Light_S , Sbot_1, Stop_1 = Extract_Masses(slha_path)                                                                                                 Masses['Glu'].append(Glu) , Masses['Neu'].append(Neu) , Masses['Light_S'].append(Light_S) , Masses['SLHA'].append(slha) 
np.save('Masses_OLD_Excluded_'     + WHAT , Masses )                                                                                                                                                        
'''

##### ALL ATLAS EXCLUDED
# loading the results
SLHA_Source = '/scratch/fambrogi/PMSSM_TGQ/'+WHAT+'_NOHIGGS_RESULTS/'

FILES = []
for name in os.listdir(SLHA_Source):
    if '.slha' in name and '.smodels' not in name and '.py' not in name:
         NAME = name
         if os.path.isfile(SLHA_Source +'/'+ NAME + '.smodels') and  os.path.isfile(SLHA_Source + '/'+ NAME + '.py'):
              FILES.append(NAME + '.py')



print '*** The total number of files excluded by ATLAS official is: ' , len(FILES)
print '\n*** Creating the numpys files containing the dictionaries \n ***'

Masses_A = {'SLHA':[] , 'Glu':[] , 'Neu':[] , 'Light_S':[] }


special_signatures = open('Not_Analised_'+WHAT+'.dat' , 'w')
special_signatures.write('# Files with special signatures or not decomposed (everything else but output_status = 1) \n')
for name in FILES: #looping over the .py results files
    slha_name = name.replace('.py','').replace('\n','')
    slha = SLHA_Source + '/' + slha_name
    slhaDOTpy = folder + '/' + name.replace('\n','')
    
    if os.path.isfile(slha):
        
        Glu, Char1, Char2, Neu2, Neu , Light_S , Sbot_1, Stop_1 = Extract_Masses(slha)
        Masses_A['Glu'].append(Glu) , Masses_A['Neu'].append(Neu) , Masses_A['Light_S'].append(Light_S) , Masses_A['SLHA'].append(slha_name)
 
np.save('Masses_ATLAS_OFF_Excluded_'     + WHAT , Masses_A )                                                                                                           
