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
#RESULTS = {'Glu':[] , 'Neu':[] , 'Light_S':[] ,
#           'T1':[] , 'T2':[] , 'T5':[] , 'T3GQon':[] ,
#            'r':[] , 'SLHA':[] }

ATLAS = np.load('Numpys/'+WHAT+'_Officially_Excluded_ATLAS-02.npy').item()
ATLAS_GLU = ATLAS['Gluino']
ATLAS_SQ = ATLAS['Squark']

RES = np.load('Numpys/ATLAS02_Excluded_BINO.npy').item()

T1_glu  = []
T2_glu  = []
T5_glu  = []
TGQ_glu = []
T2T5TGQ_glu = []
TOT_glu = []

T1_sq  = []
T2_sq  = []
T5_sq  = []
TGQ_sq = []
T2T5TGQ_sq = []
TOT_sq = []

    
rvalue = 1.0001

#print RES.keys()
T1  = RES['T1']
T5  = RES['T5']
T2  = RES['T2']
TGQ = RES['T3GQon']
GLU = RES['Glu']
SQ  = RES['Light_S']
TOT = RES['r']

print max(SQ)
for t1,t2,t5,tgq,tot,G,Q in zip(T1,T2,T5,TGQ,TOT,GLU,SQ):
        

#        print t1,t2,t5,tgq,tot,G,Q       
#	raw_input(' ')          

        if t1 > rvalue and (tot - t1) < rvalue:
            T1_glu.append(G)   , T1_sq.append(Q)  
        if t2 > rvalue and (tot-t2)< rvalue:
            T2_glu.append(G)   , T2_sq.append(Q)
        if t5 > rvalue and (tot-t5)<rvalue:
            T5_glu.append(G)   , T5_sq.append(Q)
        if tgq > rvalue and (tot-tgq) < rvalue:
            TGQ_glu.append(G)  , TGQ_sq.append(Q)

        if (t2+t5+tgq)>rvalue and (tot-(t2+t5+tgq)) < rvalue:
            T2T5TGQ_glu.append(G) , T2T5TGQ_sq.append(Q)

        if tot > rvalue:
             
            TOT_glu.append(G)  , TOT_sq.append(Q)
        if tot < rvalue:
           print 'no'



# *************************************************** Plotting part
fontsize = 20
F_legend = 12
bins = [0 + i*80 for i in range (0,100)]

lab_x_frac , lab_y_frac = 2 , 95
ymax , lab_x , lab_y = 0 , 0 , 0

xmin , ymin = 0 , 0
XMAX = 4500

if WHAT == 'HIGGSINO':
    COLOR = 'red'
if WHAT == 'BINO':
    COLOR = 'blue'

YMAX = 3000
lab_x = 200
lab_y = 2750


X_glu =      [ T1_glu, T2_glu,  T5_glu , TGQ_glu ]
X_sq  =      [ T1_sq,  T2_sq ,  T5_sq  , TGQ_sq  ]
LABELS = [ 'T1', 'T2' , 'T5',  'T3GQ' , 'T2+T5+T3GQ']                           
COLORS = [ 'blue', 'dodgerblue', 'cyan', 'green']


plt.axis([xmin, XMAX, ymin , YMAX])
LW = 1.5

# Gluino distribution
plt.grid()
print str(len(ATLAS_GLU)), str(len(TOT_glu)) , str(len(T2T5TGQ_glu))

n, bins, patches = plt.hist(ATLAS_GLU, bins, histtype='stepfilled'   , stacked= False , color = 'slateblue' , label = 'ATLAS 1508.06608', linewidth=0)
n, bins, patches = plt.hist(TOT_glu, bins, histtype='stepfilled'   , stacked= False , color = 'yellow' , label = 'All Txnames', linewidth=0)

n, bins, patches = plt.hist(T2T5TGQ_glu, bins, histtype='stepfilled'   , stacked= False , color = 'lime' , label = 'T2+T5+T3GQ', linewidth=0)
n, bins, patches = plt.hist(X_glu, bins, histtype='step'   , stacked= False  , fill = False,  color = COLORS , label = LABELS, linewidth=LW)

plt.text(lab_x, lab_y    , WHAT+'-like LSP', color = COLOR, fontsize = fontsize )

plt.ylabel('Number of Points / 80 GeV' , fontsize = fontsize-2)
plt.xlabel(r'$ m_{\tilde g }$ [GeV]'   , fontsize = fontsize+2)
plt.legend(fontsize = F_legend)
plt.savefig('PLOTS/'+ WHAT+'_Txnames_Contribution_ATLAS02_Gluino.png', dpi = 170,bbox_inches='tight' )
plt.savefig('/afs/hephy.at/user/f/fambrogi/www/TGQ_Paper/'+ WHAT+'_Txnames_Contribution_Gluino.png', dpi = 170,bbox_inches='tight' )

plt.close()

# Suqark distribution
plt.axis([xmin, XMAX, ymin , YMAX+1500])
LW = 1.5
plt.grid()
print str(len(ATLAS_GLU)), str(len(TOT_glu)) , str(len(T2T5TGQ_glu))

n, bins, patches = plt.hist(ATLAS_SQ, bins, histtype='stepfilled'   , stacked= False , color = 'slateblue' , label = 'ATLAS 1508.06608', linewidth=0)
n, bins, patches = plt.hist(TOT_sq, bins, histtype='stepfilled'   , stacked= False , color = 'yellow' , label = 'All Txnames', linewidth=0)

n, bins, patches = plt.hist(T2T5TGQ_sq, bins, histtype='stepfilled'   , stacked= False , color = 'lime' , label = 'T2+T5+T3GQ', linewidth=0)
n, bins, patches = plt.hist(X_sq, bins, histtype='step'   , stacked= False  , fill = False,  color = COLORS , label = LABELS, linewidth=LW)

WHAT = WHAT.replace('BINO','Bino').replace('HIGGSINO','Higgsino')
plt.text(lab_x, lab_y+1400    , WHAT+'-like LSP', color = COLOR, fontsize = fontsize )

plt.ylabel('Number of Points / 80 GeV' , fontsize = fontsize-2)
plt.xlabel(r'min($ m_{\tilde g }$) [GeV]'   , fontsize = fontsize+2)
plt.legend(fontsize = F_legend)
plt.savefig('PLOTS/'+ WHAT+'_Txnames_Contribution_ATLAS02_Squark.png', dpi = 170,bbox_inches='tight' )
plt.savefig('/afs/hephy.at/user/f/fambrogi/www/TGQ_Paper/'+ WHAT+'_Txnames_Contribution_Squark.png', dpi = 170,bbox_inches='tight' )

plt.close()
