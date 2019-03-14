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

import operator

from Data_Analyzer_Recast import *


parser = argparse.ArgumentParser(description='Bino or Higgsino' )
parser.add_argument('--what',  '-W', help='Bino or Higgsino'    )

args      = parser.parse_args()
WHAT     = args.what


# Keys: Heys are ['slha', 'C', 'Topo', 'w', 'Sorted', 'Neu', 'Glu', 'Light_Sq']
Dic = np.load('Numpys/Numpys_All/Missing_Topologies_'     + WHAT +'.npy' ).item()

GLU = Dic['Glu']
NEU = Dic['Neu']
VAL = Dic['w']
TOP = Dic['Topo'] 
SQU = Dic['Light_Sq']

""" Best Mising topo BINO :
BINO = [ ('[[],[[jet,jet]]]', 2254), 
('[[[jet],[jet,jet]],[[jet,jet]]]', 1142), 
('[[],[]]', 725), 
('[[[b,b]],[[jet,jet]]]', 499), 
('[[[jet]],[[jet,jet]]]', 449), 
('[[[b],[b]],[[jet],[b],[b]]]', 265), 
('[[[jet]],[[jet],[jet,jet],[jet,jet]]]', 264), 
('[[[jet],[jet,jet]],[[jet],[jet,jet]]]', 264), 
('[[[jet,jet]],[[l,nu]]]', 235) ]

HIGGSINO =  [('[[],[]]', 8576), 
('[[],[[jet,jet]]]', 1813), 
('[[[jet]],[[jet],[jet,jet]]]', 491), 
('[[[b,t]],[[jet],[b,t]]]', 188), 
('[[[b]],[[b],[jet,jet]]]', 165), 
('[[[jet]],[[jet,jet],[jet]]]', 138), 
('[[[b,b]],[[b,t]]]', 130), 
('[[[b,b]],[[jet]]]', 124), 
('[[[jet]],[[jet],[W]]]', 94), 
('[[[b]],[[t]]]', 79), 
('[[[jet],[jet]],[[jet],[jet],[jet]]]', 69), 
('[[[b,t]],[[t,t]]]', 67) ]
"""


if WHAT == 'BINO' :
   lista = { '[[],[[jet,jet]]]'                : {'Glu':[] , 'Neu':[] , 'Light_Sq':[] , 'label': '[[],[[jet,jet]]]'+ r'$(2jet + E_T ^{miss})$' , 'C': 'cyan'  } , 
             '[[[jet],[jet,jet]],[[jet,jet]]]' : {'Glu':[] , 'Neu':[] , 'Light_Sq':[] , 'label': '[[[jet],[jet,jet]],[[jet,jet]]]'+r'$(5jet + E_T ^{miss})$' , 'C': 'limegreen' } , 
             '[[[b,b]],[[jet,jet]]]'           : {'Glu':[] , 'Neu':[] , 'Light_Sq':[] , 'label': '[[[b,b]],[[jet,jet]]]'+r'$(2jet+2b+E_T ^{miss})$', 'C': 'yellow' } ,
             '[[[jet]],[[jet,jet]]]'           : {'Glu':[] , 'Neu':[] , 'Light_Sq':[] , 'label': '[[[jet]],[[jet,jet]]]'+r'$(3jet + E_T ^{miss})$' , 'C': 'slateblue'} ,
             'Other'                           : {'Glu':[] , 'Neu':[] , 'Light_Sq':[] , 'label': 'Other'  , 'C':'lightgray' } }

elif WHAT == 'HIGGSINO':
   lista = {'[[],[[jet,jet]]]'                 : {'Glu':[] , 'Neu':[] , 'Light_Sq':[] , 'label': '[[],[[jet,jet]]]'+r'$(2jet + E_T ^{miss})$' , 'C':'cyan' } ,
            '[[[jet]],[[jet],[jet,jet]]]'      : {'Glu':[] , 'Neu':[] , 'Light_Sq':[] , 'label': '[[[jet]],[[jet],[jet,jet]]]'+r'$(4jet + E_T ^{miss})$' , 'C':'dodgerblue' } ,
            '[[[b,t]],[[jet],[b,t]]]'          : {'Glu':[] , 'Neu':[] , 'Light_Sq':[] , 'label': '[[[b,t]],[[jet],[b,t]]]'+r'$(1jet+2b+2t+E_T ^{miss})$' , 'C': 'gold'} ,
            '[[[b]],[[b],[jet,jet]]]'          : {'Glu':[] , 'Neu':[] , 'Light_Sq':[] , 'label': '[[[b]],[[b],[jet,jet]]]'+r'$(2jet+2b + E_T ^{miss})$'  , 'C' : 'magenta'} ,
             'Other'                           : {'Glu':[] , 'Neu':[] , 'Light_Sq':[] , 'label': 'Other' , 'C':'lightgray'  } } 
 
for g,n,s,v,t in zip (GLU , NEU, SQU, VAL, TOP):
  v = float(v)
  if v > 1.00001:
    if t in lista.keys():
       lista[t]['Glu']     .append(g)
       lista[t]['Neu']     .append(n)
       lista[t]['Light_Sq'].append(s)
    else:
       lista['Other']['Glu']     .append(g)
       lista['Other']['Neu']     .append(n)
       lista['Other']['Light_Sq'].append(s)
  else: print 'low'    

#print lista


### Plotting part

# GLu_Neu mass plane

BINS = 10
min , MAX = 1, 10
REV = False
Marker_Size = 8
xmax, ymax = 1500 , 1000
fontsize = 21

Glu_M     = r'$m_{\tilde g}$ [GeV]'   
Neu_M     = r'$m_{\tilde{\chi}_1 ^0 }$ [GeV]'
Ch1_M     = r'$m_{\tilde \chi_1 ^{\pm} }$ [GeV]'
Light_S_M = 'min(' + r'$ m_{\tilde q }$) [GeV]'
rValue    = r'SModelS $r =\frac{\sigma_{Theo}}{\sigma_{UL}}$'


def Axis_Properties(WHAT, plt, XLABEL='x', xmin=0, XMAX=1000, YLABEL='y', ymin=0, YMAX= 1000, FONTSIZE=18, COSA = 'what is this', ana = '' , txt_1 = '', lab_x = 1 , lab_y = 1):
    
    if WHAT == 'BINO': 
       WHAT = 'Bino'
       color = 'blue'
    if WHAT == 'HIGGSINO': 
       color = 'red'
       WHAT = 'Higgsino'

    plt.xlabel(XLABEL , fontsize = FONTSIZE)
    plt.ylabel(YLABEL , fontsize = FONTSIZE)
    plt.axis([xmin, XMAX, ymin , YMAX])
    plt.text(lab_x, lab_y  , WHAT + '-like LSP'  , {'color':color , 'fontsize': FONTSIZE-4} , bbox=dict(edgecolor='white',facecolor='white'))
    plt.text(lab_x ,lab_y-YMAX/17 , txt_1      , {'color':'black' , 'fontsize': FONTSIZE-4} , bbox=dict(edgecolor='white',facecolor='white'))




if WHAT == 'BINO':
   order = list(reversed(['[[],[[jet,jet]]]','[[[jet],[jet,jet]],[[jet,jet]]]','[[[b,b]],[[jet,jet]]]','[[[jet]],[[jet,jet]]]','Other']))
   print order
elif  WHAT == 'HIGGSINO' :
   order = list(reversed(['[[],[[jet,jet]]]', '[[[jet]],[[jet],[jet,jet]]]' , '[[[b,t]],[[jet],[b,t]]]' ,'[[[b]],[[b],[jet,jet]]]','Other']))



# *********************** Glu Neu 

for t in order:
    plt.scatter(lista[t]['Glu'] , lista[t]['Neu'] , color = lista[t]['C'] , label = lista[t]['label'] , s = 10 )

Axis_Properties(WHAT , plt, XLABEL = Glu_M , xmin=0, XMAX=4000,  YLABEL= Neu_M , ymin=0, YMAX= 1200, FONTSIZE = fontsize ,
                COSA = 'what is this', ana = '' , txt_1 = '', lab_x = 2500 , lab_y = 1100 )

plt.legend(fancybox=True, fontsize = fontsize-10 , loc = 'upper left')
plt.savefig('/afs/hephy.at/user/f/fambrogi/www/TGQ_Paper/Missing/'+WHAT+'_Missing_GluNeu.png', dpi = 200, bbox_inches='tight' )
plt.close()

plt.plot()
for t in order:
    print order 
    print t
    plt.scatter(lista[t]['Glu'] , lista[t]['Neu'] , color = lista[t]['C'] , label = lista[t]['label'] , s = 10 )
Axis_Properties(WHAT , plt, XLABEL = Glu_M , xmin=200, XMAX=1500,  YLABEL= Neu_M , ymin=0, YMAX= 1200, FONTSIZE = fontsize ,
                COSA = 'what is this', ana = '' , txt_1 = '', lab_x = 1000 , lab_y = 1100 )
plt.legend(fancybox=True, fontsize = fontsize-10 , loc = 'upper left')
plt.savefig('/afs/hephy.at/user/f/fambrogi/www/TGQ_Paper/Missing/'+WHAT+'_Zoom_Missing_GluNeu.png', dpi = 200, bbox_inches='tight' )
plt.close()
# *********************** Glu Sq                                                                                                                                     

for t in order:
    plt.scatter(lista[t]['Glu'] , lista[t]['Light_Sq'] , color = lista[t]['C'] , label = lista[t]['label'] , s = 10 )

Axis_Properties(WHAT , plt, XLABEL = Glu_M , xmin=0, XMAX=4000,  YLABEL=Light_S_M , ymin=0, YMAX= 4000, FONTSIZE = fontsize ,
                COSA = 'what is this', ana = '' , txt_1 = '', lab_x = 200 , lab_y = 3700 )

plt.legend(fancybox=True, fontsize = fontsize-10 , loc = 'upper right')
plt.savefig('/afs/hephy.at/user/f/fambrogi/www/TGQ_Paper/Missing/'+WHAT+'_Missing_GluSq.png', dpi = 200, bbox_inches='tight' )
plt.close()


plt.plot()
for t in order:
    print order
    print t
    plt.scatter(lista[t]['Glu'] , lista[t]['Light_Sq'] , color = lista[t]['C'] , label = lista[t]['label'] , s = 10 )
Axis_Properties(WHAT , plt, XLABEL = Glu_M , xmin=200, XMAX=1500,  YLABEL=Light_S_M , ymin=0, YMAX= 1500, FONTSIZE = fontsize ,
                COSA = 'what is this', ana = '' , txt_1 = '', lab_x = 200 , lab_y = 1400 )
plt.legend(fancybox=True, fontsize = fontsize-10 , loc = 'upper right')
plt.savefig('/afs/hephy.at/user/f/fambrogi/www/TGQ_Paper/Missing/'+WHAT+'_Zoom_Missing_GluSq.png', dpi = 200, bbox_inches='tight' )
plt.close()
# *********************** Sq Neu                                                                                                                                    

for t in order:
    plt.scatter(lista[t]['Light_Sq'] , lista[t]['Neu'] , color = lista[t]['C'] , label = lista[t]['label'] , s = 10 )

Axis_Properties(WHAT , plt, XLABEL = Light_S_M , xmin=0, XMAX=4000,  YLABEL= Neu_M , ymin=0, YMAX= 1200, FONTSIZE = fontsize ,
                COSA = 'what is this', ana = '' , txt_1 = '', lab_x = 200 , lab_y = 1100 )

plt.legend(fancybox=True, fontsize = fontsize-10 , loc = 'upper right')
plt.savefig('/afs/hephy.at/user/f/fambrogi/www/TGQ_Paper/Missing/'+WHAT+'_Missing_SqNeu.png', dpi = 200, bbox_inches='tight' )
plt.close()

plt.plot()
for t in order:
    print order
    print t
    plt.scatter(lista[t]['Light_Sq'] , lista[t]['Neu'] , color = lista[t]['C'] , label = lista[t]['label'] , s = 10 )
Axis_Properties(WHAT , plt, XLABEL = Light_S_M , xmin=200, XMAX=1500,  YLABEL= Neu_M , ymin=0, YMAX= 1200, FONTSIZE = fontsize ,
                COSA = 'what is this', ana = '' , txt_1 = '', lab_x = 1000 , lab_y = 1100 )
plt.legend(fancybox=True, fontsize = fontsize-10 , loc = 'upper left')
plt.savefig('/afs/hephy.at/user/f/fambrogi/www/TGQ_Paper/Missing/'+WHAT+'_Zoom_Missing_SqNeu.png', dpi = 200, bbox_inches='tight' )
plt.close()
