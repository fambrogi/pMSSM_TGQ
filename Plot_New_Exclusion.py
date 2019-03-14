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

 
#Official_ATLAS   = np.load('Numpys/Numpys_All/Masses_ATLAS_OFF_Excluded_' + WHAT + '.npy').item()  # ALL points exluded by ATLAS                          
#Excluded_All     = np.load('Numpys/Numpys_All/New_ATLAS02_'               + WHAT + '.npy').item()
#Excluded_ATLAS02 = np.load('Numpys/Numpys_All/Excluded_ATLAS02_'          + WHAT + '.npy').item()
#Old_Excluded     = np.load('Numpys/Numpys_All/Masses_OLD_Excluded_'       + WHAT + '.npy').item()  # Old excluded points                                                   

             
Official_ATLAS   = np.load('Numpys/Numpys_All/Masses_ATLAS_OFF_Excluded_' + WHAT + '.npy').item()  # ALL points exluded by ATLAS                              
Excluded_All     = np.load('Numpys/Numpys_All/Excluded_ALL_'              + WHAT + '.npy').item()
#Excluded_ATLAS02 = np.load('Numpys/Numpys_All/Excluded_ATLAS02_'          + WHAT + '.npy').item()
Old_Excluded     = np.load('Numpys/Numpys_All/Old_Excluded_'              + WHAT + '.npy').item()  # Old excluded points  
Not_Now          = np.load('Numpys/Numpys_All/Excluded_Before_Not_Now_'   + WHAT + '.npy').item()



Atlas_Off_Glu , Atlas_Off_Sq = Official_ATLAS['Glu']                 , Official_ATLAS['Light_S']
Old_Excl_Glu , Old_Excl_Sq   = Old_Excluded['Glu']                   , Old_Excluded['Light_S']
New_Excl_Glu , New_Excl_Sq   = Excluded_All['Glu']+Not_Now['Glu']    , Excluded_All['Light_S']+Not_Now['Light_S']

print len(Excluded_All['Glu']), len(Not_Now['Glu']) , 'hhh'
print len(New_Excl_Glu) , len(New_Excl_Sq)
print len(Old_Excl_Glu) , len(Old_Excl_Sq)
print len(Atlas_Off_Glu) , len(Atlas_Off_Sq)


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

C1 = 'slateblue'
C2 = 'lavender'
C3 = 'cornflowerblue'
C4 = 'blue'
b = 'black'
wi = 1.1
# ******************************* GLUINO                                                                                                                                
n,bins,patches= plt.hist(Atlas_Off_Glu, bins, histtype='stepfilled' , stacked=False , fill = True,  color = C1, label = lab_excluded_ATLAS   , linewidth=0)
n,bins,patches= plt.hist(Atlas_Off_Glu, bins, histtype='step' , stacked=False , fill = False,  color = b   , linewidth=wi)

n,bins,patches= plt.hist(New_Excl_Glu,          bins, histtype='stepfilled' , stacked=False , fill = True,  color = C2, label = lab_excluded_SMO_new , linewidth=0)
n,bins,patches= plt.hist(New_Excl_Glu,          bins, histtype='step' , stacked=False , fill = False,  color = b, linewidth=wi)

n,bins,patches= plt.hist(Old_Excl_Glu,          bins, histtype='stepfilled' , stacked=False , fill = True,  color = C3, label = lab_excluded_SMO_old , linewidth=0)
n,bins,patches= plt.hist(Old_Excl_Glu,          bins, histtype='step' , stacked=False , fill = False,  color = b , linewidth=wi)


plt.ylabel('Number of Points / 80 GeV' , fontsize = fontsize-2)
plt.xlabel(r'$ m_{\tilde g }$ [GeV]'   , fontsize = fontsize+2)

#plt.legend(fontsize = fontsize-10, ncol =1)

plt.grid()
plt.axis([xmin, XMAX, ymin , YMAX])
plt.legend(fontsize = fontsize-6, ncol =1 , fancybox = True)
plt.text(lab_x, lab_y , WHAT+'-like LSP', color = COLOR, fontsize = fontsize )

plt.savefig('PLOTS/'+ WHAT+'_Comparison_Gluino.png', dpi = 200,bbox_inches='tight' )
plt.savefig('/afs/hephy.at/user/f/fambrogi/www/TGQ_Paper/'+ WHAT+'_Comparison_Gluino_aaa.png', dpi = 160,bbox_inches='tight' )
plt.close()

# with numbers in labels

# setting the LABELS                                                                                                                                                             
lab_excluded_ATLAS_n   = '['+ str(len( Atlas_Off_Glu ) ) + '] ' + 'ATLAS 1508.06680'
lab_excluded_SMO_old_n = '['+ str(len( Old_Excl_Glu  ) ) + '] ' + 'SModelS 1709.10386'                                                                                        
lab_excluded_SMO_new_n = '['+ str(len( New_Excl_Glu  ) ) + '] ' + 'SModelS with T3GQ EMs'                                                                                       

n,bins,patches= plt.hist(Atlas_Off_Glu, bins, histtype='stepfilled' , stacked=False , fill = True,  color = C1, label = lab_excluded_ATLAS_n   , linewidth=0)
n,bins,patches= plt.hist(New_Excl_Glu,          bins, histtype='stepfilled' , stacked=False , fill = True,  color = C2, label = lab_excluded_SMO_new_n , linewidth=0)
n,bins,patches= plt.hist(Old_Excl_Glu,          bins, histtype='stepfilled' , stacked=False , fill = True,  color = C3, label = lab_excluded_SMO_old_n , linewidth=0)
     
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

n,bins,patches= plt.hist(Atlas_Off_Sq, bins, histtype='stepfilled' , stacked=False , fill = True,  color = C1, label = lab_excluded_ATLAS   , linewidth=0)
n,bins,patches= plt.hist(Atlas_Off_Sq, bins, histtype='step' , stacked=False , fill = False,  color = b   , linewidth=wi)

n,bins,patches= plt.hist(New_Excl_Sq,  bins, histtype='stepfilled' , stacked=False , fill = True,  color = C2, label = lab_excluded_SMO_new , linewidth=0)
n,bins,patches= plt.hist(New_Excl_Sq,  bins, histtype='step' , stacked=False , fill = False,  color = b , linewidth=wi)

n,bins,patches= plt.hist(Old_Excl_Sq,  bins, histtype='stepfilled' , stacked=False , fill = True,  color = C3, label = lab_excluded_SMO_old , linewidth=0)
n,bins,patches= plt.hist(Old_Excl_Sq,  bins, histtype='step' , stacked=False , fill = False,  color = b , linewidth=wi)
                     
plt.ylabel('Number of Points / 80 GeV' , fontsize = fontsize-2)
plt.xlabel(r'min($m_{\tilde q }$) [GeV]'   , fontsize = fontsize+2)

plt.legend(fontsize = fontsize-10, ncol =1)

plt.grid()
plt.axis([xmin, XMAX, ymin , YMAX+1500])
plt.legend(fontsize = fontsize-9, ncol =1)
plt.text(lab_x, lab_y+1400 , WHAT+'-like LSP', color = COLOR, fontsize = fontsize )

plt.savefig('PLOTS/'+ WHAT+'_Comparison_Squark.png', dpi = 200,bbox_inches='tight' )
plt.savefig('/afs/hephy.at/user/f/fambrogi/www/TGQ_Paper/'+ WHAT+'_Comparison_Sq.png', dpi = 200,bbox_inches='tight' )

print 'Points excluded by ATLAS official :' , str(len(Atlas_Off_Glu))
print 'Points exlucded by SModelS published: ', str(len(Old_Excl_Glu))
print 'Points excluded by SModelS + T3GQ: ' , str(len(New_Excl_Glu))


