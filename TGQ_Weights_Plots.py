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


RES = np.load('Numpys/Numpys_All/Weights_NewlyExcluded_' +WHAT +'.npy').item()


T1 , T2, T5, TGQ , TOT , R = RES['T1'] , RES['T2'] , RES['T5'] , RES['T3GQ'] , RES['W'] , RES['r']




tt1 = []
tt2 = []
tt5 = []
ttgq = []
tt2tt5 = []

for t1, t2, t5, tgq, tot , r in zip(T1, T2, T5, TGQ, TOT, R):
    if t1 < 0  : t1 = 0
    if t2 < 0  : t2 = 0
    if t5 < 0  : t5  = 0
    if tgq < 0 : tgq = 0
    tt1.append( (t1/tot) * 100 )
    t2t5 = (t2+t5)/tot * 100
    ttgq.append(tgq/tot * 100 )
    tt2.append(t2)
    tt5.append(t5)
    tt2tt5.append(t2t5)


# highest r value for the topology
h_t2 = []
h_t1 = []
h_t5 = []
h_tgq = []

#2nd highest rvalue
s_t2 = []
s_t1 = []
s_t5 = []
s_tgq = []


all_res = []

# counters for the numebr of best txname
T_1, T_2 , T_5, T_GQ = 0, 0, 0, 0


for t1, t2, t5, tgq, tot , r in zip(T1, T2, T5, TGQ, TOT, R):
    if r > 5: continue
    if t1 < 0  : t1 = 0
    if t2 < 0  : t2 = 0
    if t5 < 0  : t5  = 0
    if tgq < 0 : tgq = 0

    allv = [ t1, t2, t5 , tgq ]
    best = max(allv)
 #   print best ,  ' ', allv
    allv.remove(best)
 #   print allv 
    second = max(allv)
 
    dic = {}

    if best == t1:    
       dic['t']='t1'
       T_1 = T_1 + 1
    elif best == t2:  
       dic['t']='t2'
       T_2 = T_2 + 1
    elif best == t5:  
       dic['t']='t5'
       T_5 = T_5 + 1
    elif best == tgq: 
       dic['t']='tgq'
       T_GQ = T_GQ + 1


    best = best / (t1 + t2 + t5 + tgq ) * 100
    second = second / (t1 + t2 + t5 + tgq ) * 100
  
    dic['x']=best
    dic['y']=second
    dic['z']= r

    all_res.append(dic)
    R.append(r)






def Color_Bar(plt , size = '' , bins = '' , title = '' ):
    cbar = plt.colorbar() 
    cbar.set_label( title , rotation = 90, fontsize = size)
    tick_locator = ticker.MaxNLocator(nbins=bins)
    cbar.locator = tick_locator
    cbar.update_ticks()

def Axis_Properties(WHAT, plt, XLABEL='x', xmin=0, XMAX=1000, YLABEL='y', ymin=0, YMAX= 1000, FONTSIZE=18, COSA = 'what is this', AN = 'CIAO' , lab_x = 15 , lab_y = 92):
    color = 'green'
    if WHAT == 'BINO'     : color = 'blue'
    if WHAT == 'HIGGSINO' : color = 'red'
    
    WHAT = WHAT.replace('HIGGSINO','Higgsino',).replace('BINO','Bino')
    plt.xlabel(XLABEL , fontsize = FONTSIZE)
    plt.ylabel(YLABEL , fontsize = FONTSIZE)
    plt.axis([xmin, XMAX, ymin , YMAX])
    plt.text(lab_x, lab_y  , WHAT + '-like LSP'       , {'color':color , 'fontsize': FONTSIZE-2} , bbox=dict(edgecolor='white',facecolor='white'))
    plt.text(lab_x ,lab_y - YMAX/13  , COSA        , {'color':'black' , 'fontsize': FONTSIZE-2} , bbox=dict(edgecolor='black',facecolor='white'))
    if AN != 'CIAO': plt.text(lab_x ,lab_y-YMAX/17 , AN      , {'color':'black' , 'fontsize': FONTSIZE-4} , bbox=dict(edgecolor='white',facecolor='white'))






BINS = 10
REV = False
Marker_Size = 15
SModelS_rValue = r'SModelS $r =\frac{\sigma_{Theo}}{\sigma_{UL}}$'
fontsize = 18
min, MAX = 1, 5


dic_style = { 'M': {'t1':'o' , 't2':'*', 't5':'d' , 'tgq': 'H' } ,
              'C': {'t1':'b' , 't2':'limegreen', 't5': 'magenta' , 'tgq': 'slateblue' } }

for d in all_res:
 #print d
 X = d['x']
 Y = d['y']
 Z = d['z']
 plt.scatter(X, Y, c =  Z , marker = dic_style['M'][d['t']] , s = Marker_Size ,  cmap = cm.jet,edgecolors='none' , vmin=min, vmax = MAX )

Color_Bar(plt , size = 18 , bins = BINS , title = SModelS_rValue)

plt.scatter(-10,-10 , marker = dic_style['M']['t1']  , color = 'lightgray' , s = Marker_Size , label = 'T1(' + str(T_1)+')' )
plt.scatter(-10,-10 , marker = dic_style['M']['t2']  , color = 'lightgray' , s = Marker_Size , label = 'T2(' + str(T_2)+')' )
plt.scatter(-10,-10 , marker = dic_style['M']['t5']  , color = 'lightgray' , s = Marker_Size , label = 'T5(' + str(T_5)+')' )
plt.scatter(-10,-10 , marker = dic_style['M']['tgq'] , color = 'lightgray' , s = Marker_Size , label = 'T3GQ(' + str(T_GQ)+')' )


Axis_Properties(WHAT,plt, XLABEL= 'Highest Weight [%]', xmin=30, XMAX=100, YLABEL='2nd Highest Weight [%]', ymin=0, YMAX= 60, FONTSIZE=fontsize, COSA = '' , AN='',lab_x = 32,  lab_y = 55)
plt.grid()
plt.legend(loc = 'upper right' , fontsize = fontsize-3)
plt.savefig('/afs/hephy.at/user/f/fambrogi/www/TGQ_Paper/Weights/Weight_Fraction_Experimento_r<5'+WHAT+'.png', dpi = 250, bbox_inches='tight' )
plt.close()


sorted_lists = sorted(izip(tt2, tt5 , ttgq), reverse=REV, key=lambda x: x[2])
min, MAX = 0, 100
X,Y,Z = [[x[i] for x in sorted_lists] for i in range(3)]
print X, Y , Z
plt.scatter(X, Y, c =  Z , marker = 'o', s = Marker_Size ,  cmap = cm.jet,edgecolors='none' , vmin=min, vmax = MAX )
Color_Bar(plt , size = 18 , bins = BINS , title = SModelS_rValue)
Axis_Properties(WHAT,plt, XLABEL= 'T2 Weight [%]', xmin=0, XMAX=100, YLABEL='T5 Weight [%]', ymin=0, YMAX= 100, FONTSIZE=fontsize, COSA = '' , AN='')
plt.grid()
plt.savefig('/afs/hephy.at/user/f/fambrogi/www/TGQ_Paper/Weights/Weight_Fraction_T2T5TGQ_'+WHAT+'.png', dpi = 250, bbox_inches='tight' )
plt.close()

REV = True
sorted_lists = sorted(izip(tt2, tt5 , ttgq), reverse=REV, key=lambda x: x[2])
min, MAX = 0, 100
X,Y,Z = [[x[i] for x in sorted_lists] for i in range(3)]
print X, Y , Z
plt.scatter(X, Y, c =  Z , marker = 'o', s = Marker_Size ,  cmap = cm.jet,edgecolors='none' , vmin=min, vmax = MAX )
Color_Bar(plt , size = 18 , bins = BINS , title = SModelS_rValue)
Axis_Properties(WHAT,plt, XLABEL= 'T2 Weight [%]', xmin=0, XMAX=100, YLABEL='T5 Weight [%]', ymin=0, YMAX= 100, FONTSIZE=fontsize, COSA = '' , AN='')
plt.grid()
plt.savefig('/afs/hephy.at/user/f/fambrogi/www/TGQ_Paper/Weights/Weight_Fraction_T2T5TGQ_Rev_'+WHAT+'.png', dpi = 250, bbox_inches='tight' )
plt.close()

REV = False
sorted_lists = sorted(izip(tt2tt5, ttgq , R), reverse=REV, key=lambda x: x[2])
min, MAX = 1, 10
X,Y,Z = [[x[i] for x in sorted_lists] for i in range(3)]
print X, Y , Z
plt.scatter(X, Y, c =  Z , marker = 'o', s = Marker_Size ,  cmap = cm.jet,edgecolors='none' , vmin=min, vmax = MAX )
Color_Bar(plt , size = 18 , bins = BINS , title = SModelS_rValue)
Axis_Properties(WHAT,plt, XLABEL= 'T2+T5 Weight [%]', xmin=0, XMAX=100, YLABEL='T3GQ Weight [%]', ymin=0, YMAX= 100, FONTSIZE=fontsize, COSA = '' , AN='')
plt.grid()
plt.savefig('/afs/hephy.at/user/f/fambrogi/www/TGQ_Paper/Weights/Weight_Fraction_T2+T5TGQR_'+WHAT+'.png', dpi = 250, bbox_inches='tight' )
plt.close()


'''
min, MAX = 0, 100

sorted_lists = sorted(izip(x, y , t1w), reverse=REV, key=lambda x: x[2])
print x, y , t1w
X,Y,Z = [[x[i] for x in sorted_lists] for i in range(3)]
print X, Y , Z
plt.scatter(X, Y, c =  Z , marker = 'o', s = Marker_Size ,  cmap = cm.jet,edgecolors='none' , vmin=min, vmax = MAX )
Color_Bar(plt , size = 18 , bins = BINS , title = 'T1 Weight [%]')
Axis_Properties(WHAT,plt, XLABEL= 'T2+T5 Weight [%]', xmin=0, XMAX=100, YLABEL='T3GQ Weight [%]', ymin=0, YMAX= 100, FONTSIZE=fontsize, COSA = '' , AN='')
plt.grid()
plt.savefig('/afs/hephy.at/user/f/fambrogi/www/TGQ_Paper/Weights/Weight_Fraction_T1_'+WHAT+'_''.png', dpi = 250, bbox_inches='tight' )
plt.close()
'''
