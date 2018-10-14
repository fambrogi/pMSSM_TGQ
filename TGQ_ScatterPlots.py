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
           'T1':[] , 'T2':[] , 'T5':[] , 'T3GQon':[] ,
            'r':[] , 'SLHA':[] }
print 'the total number of files is: ' , len(FILES)
lim_exclusion = 1.0000000001
if not os.path.isfile('Numpys/Numpys_All/NewlyExcluded_' +WHAT + '.npy'):
 for name in FILES: #looping over the .py results files
    slha = SLHA_Source + '/' + name + '.slha'
    slha_name = name + '.slha'
    slhaDOTpy = SLHA_Source + '/' + name.replace('\n','') +'.slha.py'
    
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
                    
                    Glu, Char1, Char2, Neu2, Neu , Light_S , Sbot_1, Stop_1 = Extract_Masses(slha)
                    
                    RESULTS['Glu'].append(Glu) , RESULTS['Neu'].append(Neu) , RESULTS['Light_S'].append(Light_S)
                    RESULTS['SLHA'].append(slha_name) , RESULTS['r'].append(r_tot)

 np.save('Numpys/Numpys_All/NewlyExcluded_' +WHAT , RESULTS)

else: 
   RESULTS = np.load('Numpys/Numpys_All/NewlyExcluded_' +WHAT + '.npy').item()

def Color_Bar(plt , size = '' , bins = '' , title = '' ):
    cbar = plt.colorbar() 
    cbar.set_label( title , rotation = 90, fontsize = size)
    tick_locator = ticker.MaxNLocator(nbins=bins)
    cbar.locator = tick_locator
    cbar.update_ticks()

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
    #plt.text(lab_x ,lab_y - YMAX/13  , COSA        , {'color':'black' , 'fontsize': FONTSIZE-4} , bbox=dict(edgecolor='black',facecolor='white'))
    plt.text(lab_x ,lab_y-YMAX/17 , txt_1      , {'color':'black' , 'fontsize': FONTSIZE-4} , bbox=dict(edgecolor='white',facecolor='white'))

def Scatter_Plot(x='', y = '' , xlabel = '', ylabel = '' , z = '', zlabel = '' , ana='' , txt_1 = '' , text = 'ciao', WHAT='' , suff = 'something' , place = ''):
    
    LAB_Y = place['lab_y']
    ymax =  place['y_max']

    sorted_lists = sorted(izip(x , y, z), reverse=REV, key=lambda x: x[2])
    X,Y,Z = [[x[i] for x in sorted_lists] for i in range(3)]
    plt.scatter(X, Y, c =  Z , marker = 'o', s = Marker_Size ,  cmap = cm.jet,edgecolors='none' , vmin=min, vmax = MAX )
    Axis_Properties(WHAT,plt, XLABEL= xlabel, xmin=200, XMAX=4000, YLABEL = ylabel, ymin=0, YMAX= ymax, FONTSIZE=fontsize+3 , ana = ana, txt_1 = text,
                    lab_x = 300 , lab_y = LAB_Y)

    Color_Bar(plt , size = 18 , bins = BINS , title = zlabel)
    plt.grid()
    plt.savefig('PLOTS/'+ WHAT + '_rValus_'+suff+'.png', dpi = 250, bbox_inches='tight' )

#/afs/hephy.at/user/f/fambrogi/www/TGQ_Paper    
    plt.savefig('/afs/hephy.at/user/f/fambrogi/www/TGQ_Paper/'+ WHAT + '_rValus_'+suff+'.png', dpi = 250, bbox_inches='tight' )
    plt.close()

# Positions of labels

PLACE_G_N = {'lab_y':1100 , 'y_max':1200}
PLACE_G_Sq = {'lab_y':3700 , 'y_max':4000}
PLACE_Sq_N = {'lab_y':1100 , 'y_max':1200}
PLACE_Glu_SqLSP = {'lab_y':130 , 'y_max':150}

BINS = 10
min , MAX = 1, 10
REV = False
Marker_Size = 8
xmax, ymax = 1500 , 1000
fontsize = 19

Glu_M     = r'$m_{\tilde g}$ [GeV]'   
Neu_M     = r'$m_{\tilde{\chi}_1 ^0 }$ [GeV]'
Ch1_M     = r'$m_{\tilde \chi_1 ^{\pm} }$ [GeV]'
Light_S_M = 'min(' + r'$ m_{\tilde q }$) [GeV]'
rValue    = r'SModelS $r =\frac{\sigma_{Theo}}{\sigma_{UL}}$'

Glu = RESULTS['Glu']
Neu = RESULTS['Neu']
Sq  = RESULTS['Light_S']
r = RESULTS['r']

print 'total number of points: ', len(r)

# Glu-Neu
a= Scatter_Plot(x=Glu,y=Neu, xlabel=Glu_M, ylabel=Neu_M     , z=r, zlabel= rValue,ana='',txt_1= '',text='',WHAT=WHAT, place=PLACE_G_N, suff='Glu_Neu')
b= Scatter_Plot(x=Glu,y=Sq , xlabel=Glu_M, ylabel=Light_S_M , z=r, zlabel= rValue,ana='',txt_1= '',text='',WHAT=WHAT, place=PLACE_G_Sq,suff='Glu_Sq')

#Glu-Sq


