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

LISTA = WHAT



# folder containing the results AND the SLHA files
folder      = WHAT+'_RESULTS'


# loading the results
SLHA_Source = folder

FILES = []
for name in os.listdir(SLHA_Source):
    if '.slha' in name and '.smodels' not in name and '.py' not in name:
         NAME = name
         if os.path.isfile(SLHA_Source +'/'+ NAME + '.smodels') and  os.path.isfile(SLHA_Source + '/'+ NAME + '.py'):
              FILES.append(NAME + '.py')



print '*** The total number of files is: ' , len(FILES)
print '\n*** Creating the numpys files containing the dictionaries \n ***'


Res_ALL        = { 'Dics':[] , 'INFO' : 'Blah Blah' } # I cant save arrays to a numpy dictionary!
Res_ATLAS02eff = { 'Dics':[] , 'INFO' : 'Blah Blah' }
Masses = {'SLHA':[] , 'Glu':[] , 'Neu':[] , 'Light_S':[] }


special_signatures = open('Not_Analised_'+WHAT+'.dat' , 'w')
special_signatures.write('# Files with special signatures or not decomposed (everything else but output_status = 1) \n')
for name in FILES: #looping over the .py results files
    slha_name = name.replace('.py','').replace('\n','')
    slha = SLHA_Source + '/' + slha_name
    slhaDOTpy = folder + '/' + name.replace('\n','')
    
    if os.path.isfile(slha):
        
      execfile(slhaDOTpy)
      Dec_Status = Check_Dec(smodelsOutput)
      
      # Extracting the rValues for the best analysis only
      if (Dec_Status == 1):
          ALL_dic, ATLAS02_dic = Extract_SModelS_Results_ALL(smodelsOutput, slha_name )
          Res_ALL['Dics'].append(ALL_dic)
          Res_ATLAS02eff['Dics'].append(ATLAS02_dic)
          #print ALL_dic, ' \n' ,  ATLAS02_dic

          # Reading the masses from the SLHAs and storing them in the dictionary
          Glu, Char1, Char2, Neu2, Neu , Light_S , Sbot_1, Stop_1 = Extract_Masses(slha)
          Masses['Glu'].append(Glu) , Masses['Neu'].append(Neu) , Masses['Light_S'].append(Light_S) , Masses['SLHA'].append(slha_name)
        
     # Writing the SLHA with special signatures in a dat file
      else: special_signatures.write(name.replace('.py','').replace('\n','') + '#' + str(Dec_Status) + ' \n')



np.save('Numpys_All/Results_ALL_'     + WHAT , Res_ALL )
np.save('Numpys_All/Results_ATLAS02_' + WHAT , Res_ATLAS02eff )
np.save('Numpys_All/Masses_'         + WHAT  , Masses )


