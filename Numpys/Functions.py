import os,sys
import pyslha2 as pyslha


Masses = { 'Neutralino'     : []    ,
           'Gluino'         : []    ,
           'Stop'           : []    ,
           'Squark'         : []    ,
           'Sbottom'        : []    ,
           'Chargino'       : []    ,
           'Neutralino2'    : []    ,
           'slha'           : []      }

def Masses_Dic (slha, Masses_Dic , Glu, Char1, Char2, Neu2, Neu , Light_S , Sbot_1, Stop_1):
    
    Masses_Dic['slha']       .append(slha)
    Masses_Dic['Neutralino'] .append(abs(Neu))
    Masses_Dic['Stop']       .append(Stop_1)
    Masses_Dic['Sbottom']    .append(Sbot_1)
    Masses_Dic['Chargino']   .append(Char1)
    Masses_Dic['Neutralino2'].append(abs(Neu2))
    Masses_Dic['Gluino']     .append(Glu)
    Masses_Dic['Squark']     .append(Light_S)



def Extract_Masses(slha):
    
    readfile = pyslha.readSLHAFile(slha)
    Glu   = readfile[0]['MASS'].entries[1000021]
    Char1 = readfile[0]['MASS'].entries[1000024]
    Char2 = readfile[0]['MASS'].entries[1000037]
    Neu = abs(readfile[0]['MASS'].entries[1000022])
    Neu2 = readfile[0]['MASS'].entries[1000023]
    
    eL, muL, eR, muR = readfile[0]['MASS'].entries[1000011],readfile[0]['MASS'].entries[1000013],readfile[0]['MASS'].entries[2000011],readfile[0]['MASS'].entries[2000013]
    
    Sbot_1 = readfile[0]['MASS'].entries[1000005]
    Stop_1 = readfile[0]['MASS'].entries[1000006]
    # ul=dl=cl=sl , ur=cr , dr=sr [valid for the pMSSM(19)]
    Sq_L   = readfile[0]['MASS'].entries[1000001]
    Sq_U_R = readfile[0]['MASS'].entries[2000002]
    Sq_D_R = readfile[0]['MASS'].entries[2000001]
    
    Light_S = min(Sq_L , Sq_U_R , Sq_D_R)
    
    return Glu, Char1, Char2, Neu2, Neu , Light_S , Sbot_1, Stop_1







def Extract_Total_Exclusion(smodelsOutput , isRes = True):
  
  ATLAS = {'best_UL_ana': 'no' ,
             'best_UL': -5,
             'best_UL_tx':'ciao',
             'best_EM_ana': 'NO',
             'best_EM': -5 ,
             'best_Fast_ana': 'No',
             'best_Fast': -9           }
             
  CMS =    {'best_UL_ana': 'no' ,
             'best_UL': -5,
             'best_UL_tx':'ciao',
             'best_EM_ana': 'NO',
             'best_EM': -5 , }

  if isRes:
    best_atlas_ana , best_atlas_ul  , best_atlas_em  = 'NO' , -5 , -6
    best_cms_ana   , best_cms_ul    , best_cms_em    = 'no' , -7 , -8
    best_Fastlim   , best_Fastlim_ana = -9, 'NO'

    for Res in smodelsOutput['ExptRes']:
            #print Res , '\n \n \n \n'
            r = []
            Type = Res['dataType']
            ana  = Res['AnalysisID']
            if 'SUS-16' in ana: continue
            if '2015' in ana: continue
            if 'SUS-15' in ana: continue
            if '2016' in ana: continue

            #print 'FF analyzing the analysis of type:' , ana, '   ' , Type
            if Type == 'upperLimit':
                #print "Res['TxNames weights (fb)']" , ana, ' ' , Type, Res['TxNames weights (fb)'] , 'UL', Res['upper limit (fb)']
               lim = Res['TxNames weights (fb)'][Res['TxNames weights (fb)'].keys()[0]] / Res['upper limit (fb)']
               #print lim , ana
               tx = Res['TxNames weights (fb)'].keys()[0]
               if 'CMS' in ana:
                   if lim > CMS['best_UL'] :
                      CMS['best_UL']     = lim
                      CMS['best_UL_ana'] = ana
                      CMS['best_UL_tx']  = tx

               elif 'ATLAS' in ana:
                   if lim > ATLAS['best_UL'] :
                       ATLAS['best_UL']     = lim
                       ATLAS['best_UL_ana'] = ana
                       ATLAS['best_UL_tx']  = tx

            elif Type == 'efficiencyMap':
                #print Res
               somma = sum(Res['TxNames weights (fb)'].values() )
               lim = somma / Res['upper limit (fb)']

               if 'CMS' in ana:
                   if lim > CMS['best_EM'] :
                      CMS['best_EM']     = lim
                      CMS['best_EM_ana'] = ana

               elif 'ATLAS' in ana:
                   if lim > ATLAS['best_EM'] :
                       ATLAS['best_EM']     = lim
                       ATLAS['best_EM_ana'] = ana
                   
                   if 'CONF' in ana:
                       if lim > ATLAS['best_Fast'] :
                           ATLAS['best_Fast_ana'] = ana
                           ATLAS['best_Fast']     = lim
                               
    return ATLAS, CMS
  else: return ATLAS, CMS










