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
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
from Data_Analyzer_Recast import Check_Dec
import pyslha2 as pyslha
from Functions import *


os.system('mkdir PLOTS')
# Select Bino or Higgsino sets
parser = argparse.ArgumentParser(description='Bino or Higgsino' )
parser.add_argument('--what',  '-W', help='Bino or Higgsino'    )

args      = parser.parse_args()
WHAT     = args.what

LISTA = WHAT

r_limit_exclusion = 1.00001

# Loading the dictionaries
Results_ALL        = np.load('Numpys/Results_ALL_'               + WHAT + '.npy').item()['Dics']         # Results for all points analised by SModelS
Results_ATLAS02    = np.load('Numpys/Results_ATLAS02_'           + WHAT + '.npy').item()['Dics'] # Results for ATLAS02 only
Masses             = np.load('Numpys/Masses_ATLAS_OFF_Excluded_' + WHAT + '.npy').item()                     # ALL points exluded by ATLAS
Old_Excluded       = np.load('Numpys/Masses_OLD_Excluded_'       + WHAT + '.npy').item()        # Old excluded points

# { 'Dics':[ RES_ALL : { 'Best_r' : -1 ,
#    'SLHA'   : SLHA }] , 'INFO' : 'Blah Blah' }

# Extracting gluinos
Neu_Atlas_Off = Masses['Neu']
Gluino_Atlas_Off = Masses['Glu']
Glu_Old          = Old_Excluded['Glu']
Glu_All = []
Glu_ATLAS02eff = []
SLHA = Masses['SLHA']


Squark_Atlas_Off = Masses['Light_S']
Squark_Old          = Old_Excluded['Light_S']
Squark_All = []
Squark_ATLAS02eff = []

Excluded_Now     = {'Glu':[] , 'Light_S':[] , 'SLHA':[] , 'Neu':[]}
Excluded_ATLAS02 = {'Glu':[] , 'Light_S':[] , 'SLHA':[] , 'Neu':[]}
 
# check if all dics are the same length
print str(len(Results_ALL)) , str(len(Results_ATLAS02)) ,str(len(Squark_Atlas_Off)) ,str(len(Gluino_Atlas_Off)) , '\n'


for all, atlas,  glu ,sq, neu, slha in zip( Results_ALL , Results_ATLAS02, Gluino_Atlas_Off, Squark_Atlas_Off ,Neu_Atlas_Off, SLHA ):
    all_r   = float(all['Best_r'])
    atlas_r = float(atlas['Best_r'])
    if all_r > r_limit_exclusion :
       Excluded_Now['Glu'].append(glu)
       Excluded_Now['Light_S'].append(sq)
       Excluded_Now['SLHA'].append(slha)
       Excluded_Now['Neu'].append(neu)

       Glu_All.append(glu)
       Squark_All.append(sq)

    if atlas_r > r_limit_exclusion :
       Glu_ATLAS02eff.append(glu)
       Squark_ATLAS02eff.append(sq)
       Excluded_ATLAS02['Glu'].append(glu)
       Excluded_ATLAS02['Light_S'].append(sq)
       Excluded_ATLAS02['SLHA'].append(slha)
       Excluded_ATLAS02['Neu'].append(neu)

print 'Saving the Dic of excluded point NOW by ALL and by ATLAS'
np.save('Numpys/Excluded_All_'    + WHAT, Excluded_Now )
np.save('Numpys/Excluded_ATLAS02_'+ WHAT, Excluded_ATLAS02 )

print len(Excluded_ATLAS02['Neu']) , len(Excluded_Now['Neu'])


'''


###############################
# Plotting part 
###############################

# Gluino plot: Gluino_Atlas_Off vs Glu_All vs Glu_ATLAS02eff vs Glu_Old
fontsize = 20
bins = [0 + i*80 for i in range (0,100)]

lab_x_frac , lab_y_frac = 2 , 95
ymax , lab_x , lab_y = 0 , 0 , 0

xmin , ymin = 0 , 0
XMAX = 4500

if WHAT == 'HIGGSINO':
    COLOR = 'red'
    WHAT = 'Higgsino'
if WHAT == 'BINO':
    COLOR = 'blue'
    WHAT = 'Bino'

YMAX = 2700
lab_x = 200
lab_y = 2450

# setting the LABELS
#lab_excluded_ATLAS   = '['+ str(len( Gluino_Atlas_Off ) ) + '] ' + 'ATLAS 1508.06608'
#lab_excluded_SMO_old = '['+ str(len( Glu_Old          ) ) + '] ' + 'SModelS 1709.10386'
#lab_excluded_SMO_new = '['+ str(len( Glu_All          ) ) + '] ' + 'SModelS with T3GQ EMs'
#only_ATLAS02         = '['+ str(len( Glu_ATLAS02eff          ) ) + '] ' + 'ATLAS-02 Only'

lab_excluded_ATLAS   = 'ATLAS 1508.06608'
lab_excluded_SMO_old = 'SModelS 1709.10386'
lab_excluded_SMO_new = 'SModelS with T3GQ EMs'
only_ATLAS02         = 'ATLAS-02 Only'

C1 = 'slateblue'
C2 = 'lavender'
C3 = 'cornflowerblue'
C4 = 'blue'

# ******************************* GLUINO                                                                                                                                                           

n,bins,patches= plt.hist(Gluino_Atlas_Off, bins, histtype='stepfilled' , stacked=False , fill = True,  color = C1, label = lab_excluded_ATLAS   , linewidth=0)
n,bins,patches= plt.hist(Glu_All,          bins, histtype='stepfilled' , stacked=False , fill = True,  color = C2, label = lab_excluded_SMO_new , linewidth=0)
n,bins,patches= plt.hist(Glu_Old,          bins, histtype='stepfilled' , stacked=False , fill = True,  color = C3, label = lab_excluded_SMO_old , linewidth=0)
#n,bins,patches= plt.hist(Glu_ATLAS02eff,   bins, histtype='step'       , stacked=False , fill = False, color = C4, label = only_ATLAS02         , linewidth=1.2)

plt.ylabel('Number of Points / 80 GeV' , fontsize = fontsize-2)
plt.xlabel(r'$ m_{\tilde g }$ [GeV]'   , fontsize = fontsize+2)

plt.legend(fontsize = fontsize-10, ncol =1)

plt.grid()
plt.axis([xmin, XMAX, ymin , YMAX])
plt.legend(fontsize = fontsize-9, ncol =1)
plt.text(lab_x, lab_y , WHAT+'-like LSP', color = COLOR, fontsize = fontsize )

plt.savefig('PLOTS/'+ WHAT+'_Comparison_Gluino.png', dpi = 200,bbox_inches='tight' )
plt.savefig('/afs/hephy.at/user/f/fambrogi/www/TGQ_Paper/'+ WHAT+'_Comparison_Gluino.png', dpi = 200,bbox_inches='tight' )
plt.close()

# with numbers in labels


# setting the LABELS                                                                                                                                                             
lab_excluded_ATLAS   = '['+ str(len( Gluino_Atlas_Off ) ) + '] ' + 'ATLAS 1508.06680'
lab_excluded_SMO_old = '['+ str(len( Glu_Old          ) ) + '] ' + 'SModelS 1709.10386'                                                                                        
lab_excluded_SMO_new = '['+ str(len( Glu_All          ) ) + '] ' + 'SModelS with T3GQ EMs'                                                                                       
only_ATLAS02         = '['+ str(len( Glu_ATLAS02eff          ) ) + '] ' + 'ATLAS-02 Only'         

n,bins,patches= plt.hist(Gluino_Atlas_Off, bins, histtype='stepfilled' , stacked=False , fill = True,  color = C1, label = lab_excluded_ATLAS   , linewidth=0)
n,bins,patches= plt.hist(Glu_All,          bins, histtype='stepfilled' , stacked=False , fill = True,  color = C2, label = lab_excluded_SMO_new , linewidth=0)
n,bins,patches= plt.hist(Glu_Old,          bins, histtype='stepfilled' , stacked=False , fill = True,  color = C3, label = lab_excluded_SMO_old , linewidth=0)
#n,bins,patches= plt.hist(Glu_ATLAS02eff,   bins, histtype='step'       , stacked=False , fill = False, color = C4, label = only_ATLAS02         , linewidth=1.2)                    
plt.ylabel('Number of Points / 80 GeV' , fontsize = fontsize-2)
plt.xlabel(r'$ m_{\tilde g }$ [GeV]'   , fontsize = fontsize+2)

plt.legend(fontsize = fontsize-10, ncol =1)

plt.grid()
plt.axis([xmin, XMAX, ymin , YMAX])
plt.legend(fontsize = fontsize-9, ncol =1)
plt.text(lab_x, lab_y , WHAT+'-like LSP', color = COLOR, fontsize = fontsize )

plt.savefig('PLOTS/'+ WHAT+'_Comparison_Gluino_numbers.png', dpi = 200,bbox_inches='tight' )
plt.savefig('/afs/hephy.at/user/f/fambrogi/www/TGQ_Paper/'+ WHAT+'_Comparison_Gluino_numbers.png', dpi = 200,bbox_inches='tight' )
plt.close()


# ******************************* SQUARKS

n,bins,patches= plt.hist(Squark_Atlas_Off, bins, histtype='stepfilled' , stacked=False , fill = True,  color = C1, label = lab_excluded_ATLAS   , linewidth=0)
n,bins,patches= plt.hist(Squark_All,          bins, histtype='stepfilled' , stacked=False , fill = True,  color = C2, label = lab_excluded_SMO_new , linewidth=0)
n,bins,patches= plt.hist(Squark_Old,          bins, histtype='stepfilled' , stacked=False , fill = True,  color = C3, label = lab_excluded_SMO_old , linewidth=0)
#n,bins,patches= plt.hist(Glu_ATLAS02eff,   bins, histtype='step'       , stacked=False , fill = False, color = C4, label = only_ATLAS02         , linewidth=1.2)                                     

plt.ylabel('Number of Points / 80 GeV' , fontsize = fontsize-2)
plt.xlabel(r'min($m_{\tilde q }$) [GeV]'   , fontsize = fontsize+2)

plt.legend(fontsize = fontsize-10, ncol =1)

plt.grid()
plt.axis([xmin, XMAX, ymin , YMAX+1500])
plt.legend(fontsize = fontsize-9, ncol =1)
plt.text(lab_x, lab_y+1400 , WHAT+'-like LSP', color = COLOR, fontsize = fontsize )

plt.savefig('PLOTS/'+ WHAT+'_Comparison_Squark.png', dpi = 200,bbox_inches='tight' )
plt.savefig('/afs/hephy.at/user/f/fambrogi/www/TGQ_Paper/'+ WHAT+'_Comparison_Squark.png', dpi = 200,bbox_inches='tight' )

print 'Points excluded by ATLAS official :' , str(len(Squark_Atlas_Off))
print 'Points exlucded by SModelS published: ', str(len(Squark_Old))
print 'Points excluded by SModelS + T3GQ: ' , str(len(Squark_All))







'''
