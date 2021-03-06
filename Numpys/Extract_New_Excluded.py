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

FILES = []
for name in os.listdir(SLHA_Source):
    if '.slha' in name and '.smodels' not in name and '.py' not in name:
         NAME = name
         if os.path.isfile(SLHA_Source +'/'+ NAME + '.smodels') and  os.path.isfile(SLHA_Source + '/'+ NAME + '.py'):
              FILES.append(NAME + '.py')



print '*** The total number of files is: ' , len(FILES)
print '\n*** Creating the numpys files containing the dictionaries \n ***'

Res_ALL     = { 'r':[] , 'Glu':[] , 'Neu':[], 'SLHA':[] , 'Light_S':[] , 'INFO': 'Blah Blah' } # I cant save arrays to a numpy dictionary!
Res_ATLAS02 = { 'r':[] , 'Glu':[] , 'Neu':[], 'SLHA':[] , 'Light_S':[] , 'INFO': 'Blah Blah' }
Excluded_ALL     = { 'r':[] , 'Glu':[] , 'Neu':[], 'SLHA':[] , 'Light_S':[] , 'INFO': 'Blah Blah' } # I cant save arrays to a numpy dictionary!                 
Excluded_ATLAS   = { 'r':[] , 'Glu':[] , 'Neu':[], 'SLHA':[] , 'Light_S':[] , 'INFO': 'Blah Blah' } # I cant save arrays to a numpy dictionary!                    

# Listing Special Signature points
rvalue_limit = 1.00001

special_signatures = open('Not_Analised_'+WHAT+'.dat' , 'w')
special_signatures.write('# Files with special signatures or not decomposed (everything else but output_status = 1) \n')

for name in FILES: #looping over the .py results files
    slha_name = name.replace('.py','').replace('\n','')
    slha = SLHA_Source + '/' + slha_name
    slhaDOTpy = SLHA_Source + '/' + name.replace('\n','')
    
    if os.path.isfile(slha):
        
      execfile(slhaDOTpy)
      Dec_Status = Check_Dec(smodelsOutput)
      
      # Extracting the rValues for the best analysis only
      if (Dec_Status == 1):
          ALL_dic, ATLAS02_dic = Extract_SModelS_Results_ALL(smodelsOutput, slha_name )
          #print ALL_dic.keys()
          r_all , r_atlas = float(ALL_dic['Best_r']) , float(ATLAS02_dic['Best_r'])

          # Reading the masses from the SLHAs and storing them in the dictionary
          Glu, Char1, Char2, Neu2, Neu , Light_S , Sbot_1, Stop_1 = Extract_Masses(slha)

          Res_ALL['r'].append(r_all)
          Res_ALL['Glu'].append(Glu)
          Res_ALL['Neu'].append(Neu)
          Res_ALL['Light_S'].append(Light_S)
          Res_ALL['SLHA'].append(slha_name)

          Res_ATLAS02['r'].append(r_atlas)
          Res_ATLAS02['Glu'].append(Glu)
          Res_ATLAS02['Neu'].append(Neu)
          Res_ATLAS02['Light_S'].append(Light_S)
          Res_ATLAS02['SLHA'].append(slha_name)

          if r_all > rvalue_limit:
              #print r_all , rvalue_limit , slha_name 

              Excluded_ALL['r'].append(r_all)
              Excluded_ALL['Glu'].append(Glu)
              Excluded_ALL['Neu'].append(Neu)
              Excluded_ALL['Light_S'].append(Light_S)
              Excluded_ALL['SLHA'].append(slha_name)
          if r_atlas > rvalue_limit:

              Excluded_ATLAS['r'].append(r_atlas)
              Excluded_ATLAS['Glu'].append(Glu)
              Excluded_ATLAS['Neu'].append(Neu)
              Excluded_ATLAS['Light_S'].append(Light_S)
              Excluded_ATLAS['SLHA'].append(slha_name)
        
     # Writing the SLHA with special signatures in a dat file
      else: special_signatures.write(name.replace('.py','').replace('\n','') + '#' + str(Dec_Status) + ' \n')


special_signatures.close()

np.save('Numpys_All/New_ALL_'+WHAT, Res_ALL)
np.save('Numpys_All/New_ATLAS02_'+WHAT, Res_ATLAS02)

np.save('Numpys_All/Excluded_ALL_'+WHAT, Excluded_ALL)
np.save('Numpys_All/Excluded_ATLAS02_'+WHAT, Excluded_ATLAS)


print 'total  NEW : '     , len(Res_ALL['SLHA'])
print 'total  ATLAS02 : ' , len(Res_ATLAS02['SLHA'])

print 'total  Excluded NEW : '     , len(Excluded_ALL['SLHA'])
print 'total  Excluded ATLAS02 : ' , len(Excluded_ATLAS['SLHA'])
