import os,sys
import pyslha2 as pyslha
import itertools

'''
txNames_CMS = [ 'T1tttt-EM','T1-EM', 'T1btbt-EM' , 'T1bbbb-EM',
                'T2-EM'    , 'T2bb-EM' , 'T2tt-EM'   , 'T6bbWW-EM', 'T6bbWWoff-EM',
                'T5-EM'    , 'T5bbbb-EM', 'T5tttt-EM', 'T5WW-EM', 'T5WWoff-EM', 'T5ZZ-EM',
                'TChiWW-EM', 'TChiWZ-EM', 'TChiZZ-EM'  ]
'''

txNames_CMS =   [ 'T1tttt-EM','T1-EM', 'T1btbt-EM' , 'T1bbbb-EM',
                 'T2-EM'    , 'T2bb-EM' , 'T2tt-EM'  , 'T2bt-EM',
                 'T5-EM'    , 'T5bbbb-EM', 'T5tttt-EM', 'T5WW-EM', 'T5WWoff-EM', 'T5ZZ-EM',
                 'TChiWW-EM', 'TChiWZ-EM', 'TChiZZ-EM', 
                 'T6WW-EM', 'T6WWoff-EM',  # squarks cascade
                 'T6bbWW-EM' , 'T6bbWWoff-EM' ,    # cascade 3rd generation
                 'T6ZZtt-EM' , 'T6ZZttoff-EM', 'T6ttZZ-EM' , 'T6ttWW-EM' ,
                 'T6ttWWoff-EM' , 'T6ttoffWW-EM', 'T6WWtt-EM' , 'T6WWttoff-EM',
                 'T6WWofftt-EM', 'T6bbZZ-EM', 'T6bbZZoff-EM', 'T6ZZbb-EM' , 'T6ZZoffbb-EM',
                 'T3GQon-EM' , 'TGN-EM'] # TGQ



txNames_ATLAS047 =       [ 'T1-EM' , 'T1bbbb-EM',  'T1bbbt-EM', 'T1bbqq-EM', 'T1bbtt-EM', 'T1btbt-EM', 'T1btqq-EM', 'T1bttt-EM', 'T1qqtt-EM', 'T1tttt-EM',
                          'T2-EM' , 'T2bb-EM'  ,  'T2bt-EM'  , 'T2tt-EM'  , 'T5bbbb-EM', 'T5bbbt-EM', 'T5btbt-EM', 'T5tbtb-EM', 'T5tbtt-EM', 'T5tttt-EM',
                          'TGQ-EM', 'TGQbbq-EM',  'TGQbtq-EM', 'TGQqtt-EM']



'''
    # Prototype of a CompleteRes
    DIC = {'Point':slha , 'Glu' : 0, 'Neu' : 0,
    'CMS-SUS-13-012': {    'T1tttt-UL': -1 , 'T1-UL'    : -1 , 'T2-UL': -1   ,
    'EM' : {
    'T1-EM': 0       , 'T1tttt-EM': 0 , 'T2-EM': 0,
    'T2bb-EM'  : 0   , 'T2tt-EM'  : 0 , 'T6bbWW-EM': 0 ,
    'T1btbt-EM': 0   , 'T1bbbb-EM': 0 ,
    'T5bbbb-EM': 0   , 'T5tttt-EM': 0 , 'T5-EM' : 0, 'T5WW-EM': 0, 'T5WWoff-EM': 0, 'T5ZZ-EM': 0,
    'TChiWW-EM': 0   , 'TChiZZ-EM': 0 , 'TChiWZ-EM' : 0 }
    
    } }

'''
#####################
# GENERAL UTILITIES #
#####################

# This reads the masses of gluiino, chargino1 and 2, and neutralino
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


def Extract_rValue_txName_New(Res, txName = '', analysis='', type = ''):
    r = [-1]
    if Res['dataType'] == 'upperLimit':
        
           if Res['AnalysisID']== analysis and Res['TxNames weights (fb)'].keys()[0] == txName :
                   lim = Res['TxNames weights (fb)'][txName] / Res['upper limit (fb)']
                   r.append(Res['TxNames weights (fb)'][txName] / Res['upper limit (fb)'])
    #print Res['TxNames weights (fb)'][txName] / Res['upper limit (fb)']
                   # print Res['TxNames weights (fb)'][txName]
                   # print Res['upper limit (fb)']
                   # print 'the r vector is', r
                   # print 'the max is', max(r)
    elif Res['dataType'] == 'efficiencyMap':
                if Res['AnalysisID']== analysis:
                    for key in Res['TxNames weights (fb)'].keys():
                        if key == txName:
                           r.append(Res['TxNames weights (fb)'][txName] / Res['upper limit (fb)'])
    return max(r)




# This checks the decomposition status
def Check_Dec(smodelsOutput):
    status = smodelsOutput['OutputStatus']['decomposition status']
    return status


# Check if the ANALYSIS is in the list of Results
def Is_Res(smodelsOutput, ANALYSIS):
    Is_Result = False
    for Res in smodelsOutput['ExptRes']:
        if (Res['AnalysisID'] == ANALYSIS):
            Is_Result = True
    return Is_Result


# Creates a list of results from the single point dictionary
# To be called on top of the script , same for any analysis
def Extract_Res_Recast(Complete_Res , txNames = '' , ANALYSIS = ''):
    Dic_Lists = {'UL': [], 'Tot_EM':[] , 'Glu':[] , 'Neu':[] , 'SLHA':[] , 'Light_S':[] , 'Stop':[] , 'Sbot':[] , 'Ch1':[] , 'Neu2':[] , 'T1_UL':[], 'T2_UL':[]}
    # Create a list for each txNames, with their rValues, that is appended to the Dic_Lists dictionary
    for tx in txNames:
        name = tx
        tx = {'rValues':[] }
        Dic_Lists[name] = tx
    for dic in Complete_Res:
        Tot_Weight = 0
        for tx in txNames:
            
            Dic_Lists[tx]['rValues'].append(dic[ANALYSIS]['EM'][tx])
            Tot_Weight = Tot_Weight + dic[ANALYSIS]['EM'][tx]
        Dic_Lists['SLHA']   .append(dic['Point'])
        Dic_Lists['Glu']    .append(dic['Glu'])
        Dic_Lists['Neu']    .append(abs(dic['Neu']))
        Dic_Lists['Neu2']   .append(abs(dic['Neu2']))
        Dic_Lists['Ch1']    .append(dic['Ch1'])
        Dic_Lists['Stop']   .append(dic['Stop'])
        Dic_Lists['Sbot']   .append(dic['Sbot'])
        Dic_Lists['Light_S'].append(dic['Light_S'])

        Dic_Lists['Tot_EM']    .append(Tot_Weight)
        Dic_Lists['UL']        .append(dic[ANALYSIS]['UL'] )
        Dic_Lists['T1_UL']     .append(dic[ANALYSIS]['UL'] )
        Dic_Lists['T2_UL']     .append(dic[ANALYSIS]['UL'] )


    return Dic_Lists



# Extract the list of results for each SLHA
def Extract_SModelS_Results_ALL(smodelsOutput,SLHA = ''):
    RES_ALL = { 'Best_r' : -1 ,
                'SLHA'   : SLHA }

    RES_ATLAS02eff = { 'Best_r' : -1 ,
                    'SLHA'   : SLHA }

    Rs = []
    for Res in smodelsOutput['ExptRes']:
         AN   = Res['AnalysisID']
         r    = Res['r']
         Type = Res['dataType']
         Rs.append(r)

         if AN == 'ATLAS-SUSY-2013-02' and Type =='efficiencyMap':
            RES_ATLAS02eff['Best_r'] = r



    RES_ALL['Best_r'] = max(Rs) # extracting the best r value

    return RES_ALL , RES_ATLAS02eff





#######
# CMS #
#######
def Extract_Analysis_ResCMS012(smodelsOutput, ANALYSIS='CMS-SUS-13-012',TXNAMES = txNames_CMS , WHAT = ''):
    T1tttt_UL , T1_UL , T2_UL = [-1],[-1],[-1]
    EMs = { }
    for name in txNames_CMS: # I create a dic for each txNames of the EMs results
        a=[0]
        EMs[name] = a
    for Res in smodelsOutput['ExptRes']:
        if (Res['AnalysisID'] == ANALYSIS):
           Type = Res['dataType']
           for txName in TXNAMES: # for each txName in the resu list, I append the real values, -1 otherwise
            if Type == 'efficiencyMap' :
                     EMs[txName].append(Extract_rValue_txName_New(Res,txName.replace('-EM','') ,analysis= ANALYSIS, type = Type))
            if Type == 'upperLimit':
                if   (txName == 'T1-EM'):
                     lim = Extract_rValue_txName_New(Res,txName = 'T1' , analysis= ANALYSIS, type = Type )
                     T1_UL.append(lim)
                elif (txName == 'T2-EM'):
                     lim = Extract_rValue_txName_New(Res,txName = 'T2' , analysis= ANALYSIS, type = Type )
                     T2_UL.append( lim )
                elif (txName == 'T1tttt-EM'):
                     lim = Extract_rValue_txName_New(Res,txName = 'T1tttt' , analysis= ANALYSIS, type = Type )
                     T1tttt_UL.append( lim )
#print max(T1tttt_UL) , max(T1_UL) , max(T2_UL), EMs
    return EMs





def Extract_SModelS_Results_CMS012(smodelsOutput,slha,decomposed=0, ANALYSIS = 'CMS-SUS-13-012', TXNAMES = txNames_CMS, WHAT = ''):
    DIC = {'Point':slha , 'Glu':0, 'Neu':0, 'Ch1': 0, 'Light_S':0 , 'Stop':0 , 'Sbot':0 , 'Ch1':0 , 'Neu2':0,
           ANALYSIS: { 'UL':-1,  'T1tttt-UL': -1 , 'T1-UL'    : -1 , 'T2-UL': -1   ,
           'EM': {
                                     'T1-EM': 0, 'T1tttt-EM': 0, 'T1btbt-EM': 0   , 'T1bbbb-EM': 0 , 'TGN-EM':0,                      # direct gluinos
                                     'T5bbbb-EM': 0   , 'T5tttt-EM': 0 , 'T5-EM' : 0, 'T5WW-EM': 0, 'T5WWoff-EM': 0, 'T5ZZ-EM': 0,  # cascade gluinos

                                     'T2-EM': 0, 'T2bb-EM'  : 0   , 'T2tt-EM'  : 0 , 'T2bt-EM':0, #direct squarks
                                     
                                     'T6WW-EM':0  , 'T6WWoff-EM': 0,  # squarks cascade
                                     'T6bbWW-EM':0  , 'T6bbWWoff-EM': 0 ,    # cascade 3rd generation
                                     'T6ZZtt-EM':0  , 'T6ZZttoff-EM': 0,
                                     'T6ttZZ-EM':0  ,
                                     'T6ttWW-EM':0  , 'T6ttWWoff-EM':0, 'T6ttoffWW-EM':0 ,
                                     'T6WWtt-EM':0  , 'T6WWttoff-EM':0, 'T6WWofftt-EM':0 ,
                                     'T6bbZZ-EM':0  , 'T6bbZZoff-EM':0,
                                     'T6ZZbb-EM':0  , 'T6ZZoffbb-EM':0,
                                     
                                     'TChiWW-EM': 0   , 'TChiZZ-EM': 0 , 'TChiWZ-EM' : 0 ,  # EWikinos
                            
                                     
                                     'T3GQon-EM': 0 }}} # TGQ {


    if (decomposed==1):
       Glu, Char1, Char2, Neu2, Neu , Light_S , Sbot_1, Stop_1 = Extract_Masses(slha) # Filling the masses (only Glu and Neutralinos for now)
       
       DIC['Glu'], DIC['Neu'], DIC['Ch1'], DIC['Light_S'], DIC['Stop'], DIC['Sbot'], DIC['Neu2'] = Glu, abs(Neu) , Char1 , Light_S , Stop_1, Sbot_1, Neu2
       Res = smodelsOutput['ExptRes']
       if Is_Res(smodelsOutput, 'CMS-SUS-13-012'):
              T1tttt_UL, T1_UL, T2_UL = Extract_UL_oldResults(slha = slha , ANALYSIS = ANALYSIS , TXNAMES = TXNAMES)
              DIC[ANALYSIS]['T1-UL'] = T1_UL
              DIC[ANALYSIS]['T2-UL'] = T2_UL
              DIC[ANALYSIS]['T1tttt-UL'] = T1tttt_UL
              DIC[ANALYSIS]['UL']    = max(T1_UL, T2_UL , T1tttt_UL)
              
              EMs = Extract_Analysis_ResCMS012(smodelsOutput, ANALYSIS='CMS-SUS-13-012' )
              for name in TXNAMES:
                 DIC['CMS-SUS-13-012']['EM'][name] = max(EMs[name])
              return DIC


def Extract_UL_oldResults (slha = '' , ANALYSIS = '', TXNAMES = ''):
    T1tttt_UL , T1_UL , T2_UL = [-1],[-1],[-1]
    slhaDOTpy_ul = slha.replace('\n','') + '.py'
    execfile(slhaDOTpy_ul , globals())  # witouth globals it does not store the variable
    Dec_Status = Check_Dec(smodelsOutput)
    
    if not Dec_Status == 1: return T1tttt_UL , T1_UL , T2_UL # this is a dobule check
    for Res in smodelsOutput['ExptRes']:
        if (Res['AnalysisID'] == ANALYSIS):
           Type = Res['dataType']
           for txName in TXNAMES: # for each txName in the resu list, I append the real values, -1 otherwise
            if Type == 'upperLimit':
                if   (txName == 'T1-EM'):
                     lim = Extract_rValue_txName_New(Res,txName = 'T1' , analysis= ANALYSIS, type = Type )
                     T1_UL.append(lim)
                elif (txName == 'T2-EM'):
                     lim = Extract_rValue_txName_New(Res,txName = 'T2' , analysis= ANALYSIS, type = Type )
                     T2_UL.append( lim )
                elif (txName == 'T1tttt-EM'):
                     lim = Extract_rValue_txName_New(Res,txName = 'T1tttt' , analysis= ANALYSIS, type = Type )
                     T1tttt_UL.append( lim )
#print max(T1tttt_UL) , max(T1_UL) , max(T2_UL), EMs
    return max(T1tttt_UL) , max(T1_UL) , max(T2_UL)




'''

#########
# ATLAS #
#########
def Extract_SModelS_Results_ATLAS047(smodelsOutput,slha,decomposed=0, ANALYSIS = 'ATLAS-CONF-2013-047', TXNAMES = txNames_ATLAS047):
    DIC = {'Point':slha , 'Glu':0, 'Neu':0, 'Ch1': 0, 'Light_S':0 , 'Stop':0 , 'Sbot':0 , 'Ch1':0 , 'Neu2':0,
        
           ANALYSIS: {  'UL':-1,  'T1-UL': -1 , 'T2-UL'    : -1,
               'EM' : { 'T1-EM' :0 ,'T1bbbb-EM':0, 'T1bbbt-EM':0, 'T1bbqq-EM':0, 'T1bbtt-EM':0, 'T1btbt-EM':0, 'T1btqq-EM':0, 'T1bttt-EM':0, 'T1qqtt-EM':0, 'T1tttt-EM':0,
                        'T2-EM' :0 ,'T2bb-EM'  :0, 'T2bt-EM'  :0, 'T2tt-EM'  :0, 'T5bbbb-EM':0, 'T5bbbt-EM':0, 'T5btbt-EM':0, 'T5tbtb-EM':0, 'T5tbtt-EM':0, 'T5tttt-EM':0,
                        'TGQ-EM':0 ,'TGQbbq-EM':0, 'TGQbtq-EM':0, 'TGQqtt-EM':0 }

} }
    if (decomposed==1):
       Glu, Char1, Char2, Neu2, Neu , Light_S , Sbot_1, Stop_1 = Extract_Masses(slha) # Filling the masses (only Glu and Neutralinos for now)
       DIC['Glu'], DIC['Neu'], DIC['Ch1'], DIC['Light_S'], DIC['Stop'], DIC['Sbot'], DIC['Neu2'] = Glu, abs(Neu) , Char1 , Light_S , Stop_1, Sbot_1, Neu2
       Res = smodelsOutput['ExptRes']
       if Is_Res(smodelsOutput, ANALYSIS):
          T1_UL, T2_UL, EMs = Extract_Analysis_Res_ATLAS047(smodelsOutput, ANALYSIS='ATLAS-CONF-2013-047')
          DIC[ANALYSIS]['T1-UL'] = T1_UL
          DIC[ANALYSIS]['T2-UL'] = T2_UL
          DIC[ANALYSIS]['UL']    = max(T1_UL, T2_UL)
          for name in TXNAMES:
              DIC[ANALYSIS]['EM'][name] = max(EMs[name]) # It should be just one value, but I pick up the max so that I am sure
    return DIC

'''

'''
    Example of Dic_Lists
{'SLHA': ['Bino_fixSlep//100042885.slha'], 'T5WW-EM': {'rValues': [0]}, 'TChiZZ-EM': {'rValues': [0]}, 'T5ZZ-EM': {'rValues': [0]}, 'T5tttt-EM': {'rValues': [0]}, 'T6bbWW-EM': {'rValues': [0]}, 'Tot_EM': [0], 'TChiWZ-EM': {'rValues': [0]}, 'T2bb-EM': {'rValues': [0]}, 'T5-EM': {'rValues': [0]}, 'T5bbbb-EM': {'rValues': [0]}, 'TChiWW-EM': {'rValues': [0]}, 'T5WWoff-EM': {'rValues': [0]}, 'T1tttt-EM': {'rValues': [0]}, 'T2-EM': {'rValues': [0]}, 'T1-EM': {'rValues': [0]}, 'T2tt-EM': {'rValues': [0]}, 'Neu': [584.111445], 'T1bbbb-EM': {'rValues': [0]}, 'Glu': [594.699912], 'T1btbt-EM': {'rValues': [0]}}
'''

# USed for the histograms of the exclusions!
def Extract_Exluded_By(Dic_Lists, txName):
    #txName = txName + '-EM'
    Tx_r, Tx_g, Tot_EM , Ul , Slha = Dic_Lists[txName]['rValues'] , Dic_Lists['Glu'] , Dic_Lists['Tot_EM'] , Dic_Lists['UL'] , Dic_Lists['SLHA']

    Excluded_Only_EM = { txName : [] , 'Glu' : [] , 'SLHA':[] } # this is for comparing exclusion irrespectively if the point is excluded already by UL
    Excluded_Only_UL = { txName : [] , 'Glu' : [] , 'SLHA':[] } # here we do not consider points already excluded by UL results

    for r, glu, tot, ul, slha in zip(Tx_r, Tx_g, Tot_EM , Ul , Slha) :
        if (r > 1 and (tot - r) < 1):
            Excluded_Only_EM[txName].append(r) ,  Excluded_Only_EM['Glu'].append(glu) , Excluded_Only_EM['SLHA'].append(slha)
        if (r > 1 and (tot - r) < 1 and ul < 1): # UL UNCONSTRAINED !!!!
            Excluded_Only_UL[txName].append(r) ,  Excluded_Only_UL['Glu'].append(glu) , Excluded_Only_UL['SLHA'].append(slha)

    return Excluded_Only_EM , Excluded_Only_UL

# Extracts dictionaries of excluded by categories
def Extract_TotalExclusion(Dic_Lists):

#print Dic_Lists
    Excluded_by_EM        = { 'rValue' : [] , 'Glu' : [] , 'SLHA':[] }
    Excluded_by_UL        = { 'rValue' : [] , 'Glu' : [] , 'SLHA':[] }
    Excluded_by_UL_or_EM  = { 'rValue' : [] , 'Glu' : [] , 'SLHA':[] }
    Excluded_by_EM_only   = { 'rValue' : [] , 'Glu' : [] , 'SLHA':[] }
    Excluded_by_UL_only   = { 'rValue' : [] , 'Glu' : [] , 'SLHA':[] }

    Tx_g, Tot_EM , Ul , Slha = Dic_Lists['Glu'] , Dic_Lists['Tot_EM'] , Dic_Lists['UL'] , Dic_Lists['SLHA']

#print "Dic_Lists['UL'] ***************** " , Dic_Lists['UL']
    for glu, tot, ul, slha in zip( Tx_g, Tot_EM , Ul , Slha) :
        if (tot >= 1 ):
            Excluded_by_EM['rValue'].append(tot) ,  Excluded_by_EM['Glu'].append(glu) , Excluded_by_EM['SLHA'].append(slha)
        if (ul >= 1 ):
            Excluded_by_UL['rValue'].append(ul) ,  Excluded_by_UL['Glu'].append(glu) , Excluded_by_UL['SLHA'].append(slha)
        if ( max(tot,ul)>=1):
            Excluded_by_UL_or_EM['rValue'].append(max(tot,ul)) ,  Excluded_by_UL_or_EM['Glu'].append(glu) , Excluded_by_UL_or_EM['SLHA'].append(slha)
        if ( tot >=1 and ul < 1):
            Excluded_by_EM_only['rValue'].append(max(tot,ul)) ,  Excluded_by_EM_only['Glu'].append(glu) , Excluded_by_EM_only['SLHA'].append(slha)
        if ( tot < 1 and ul >= 1):
            Excluded_by_UL_only['rValue'].append(max(tot,ul)) ,  Excluded_by_UL_only['Glu'].append(glu) , Excluded_by_UL_only['SLHA'].append(slha)

    return Excluded_by_EM , Excluded_by_UL, Excluded_by_UL_or_EM, Excluded_by_EM_only, Excluded_by_UL_only

#Pairs of txNames
# ('T5WWoff-EM', 'T5ZZ-EM') PAIR EXTRACTED
'''
    Recast results
{'SLHA': ['Bino_fixSlep//100042885.slha'], 'T5tttt-EM': {'rValues': [0]}, 'T1tttt-EM': {'rValues': [0]}, 'T1-EM': {'rValues': [0]}, 'T2tt-EM': {'rValues': [0]}, 'Neu': [584.111445], 'TChiWW-EM': {'rValues': [0]}, 'T2bb-EM': {'rValues': [0]}, 'T5bbbb-EM': {'rValues': [0]}, 'T5WWoff-EM': {'rValues': [0]}, 'TChiZZ-EM': {'rValues': [0]}, 'T5-EM': {'rValues': [0]}, 'T5WW-EM': {'rValues': [0]}, 'Tot_EM': [0], 'TChiWZ-EM': {'rValues': [0]}, 'T2-EM': {'rValues': [0]}, 'T1bbbb-EM': {'rValues': [0]}, 'Glu': [594.699912], 'T6bbWW-EM': {'rValues': [0]}, 'T5ZZ-EM': {'rValues': [0]}, 'UL': [-1], 'T1btbt-EM': {'rValues': [0]}}

txNames_CMS = [ 'T1tttt-EM','T1-EM','T2-EM', 'T2bb-EM' , 'T2tt-EM' , 'T6bbWW-EM', 'T1btbt-EM' , 'T1bbbb-EM',
'T5-EM', 'T5bbbb-EM', 'T5tttt-EM' , 'T5WW-EM', 'T5WWoff-EM', 'T5ZZ-EM', 'TChiWW-EM', 'TChiWZ-EM', 'TChiZZ-EM'  ]
'''

# This script extracts all the possible doublets of txnames results given a list, and adds up the weights of the two.
def Excluded_By_Doublets(Dic_Lists,txNames):

#    txNames_CMS = ['T1-EM','T2-EM', 'T5-EM', ]
    
    All_Combo_Dic = {'Glu':[], 'SLHA':[]}
    Combo_Pairs = list(itertools.combinations(txNames, 2))
    
    Combo_Pair_Names = []
    for pair in Combo_Pairs:
        name = pair[0].replace('-EM','') + '+' + pair[1].replace('-EM','')
        tx1, tx2 = pair[0] , pair[1]
        All_Combo_Dic[name] = { 'Name': name , 'rValues': [] }
        Combo_Pair_Names.append(name)
    
    for g,s in zip(Dic_Lists['Glu'], Dic_Lists['SLHA'] ):
        All_Combo_Dic['Glu'].append(g)
        All_Combo_Dic['SLHA'].append(s)
        for pair in Combo_Pairs:
            index = Dic_Lists['Glu'].index(g)
            name = pair[0].replace('-EM','') + '+' + pair[1].replace('-EM','')
            tx1, tx2 = pair[0] , pair[1]
            R1 = Dic_Lists[tx1]['rValues'][index]
            R2 = Dic_Lists[tx2]['rValues'][index]
            R = R1 + R2
            All_Combo_Dic[name]['rValues'].append(R)

    All_Combo_Dic['Tot_EM'] = Dic_Lists['Tot_EM'] # I add the total rValue from EM
    All_Combo_Dic['UL'] = Dic_Lists['UL'] # I add the total rValue from EM

    return All_Combo_Dic

def Check_Doublet_Only_Exclusion(tx1tx2 , Recast_Results, Doublets):
    tx1 , tx2 = tx1tx2.split('+')[0]+'-EM' , tx1tx2.split('+')[1]+'-EM'
    EM = tx1+tx2+'_EM_Only'
    EMr = []
    UL = tx1+tx2+'_EM_UL'
    ULr = []
    
    T1_R , T1_Glu = Recast_Results[tx1]['rValues'] , Recast_Results['Glu']
    T2_R , T2_Glu = Recast_Results[tx2]['rValues'] , Recast_Results['Glu']
    T1_T2         = Doublets[tx1tx2]['rValues']
    Tot_EM        = Doublets['Tot_EM']
    UL            = Doublets['UL']
    
    for t1, t2, t1t2, em, ul, g in zip(T1_R , T2_R , T1_T2, Tot_EM, UL , T1_Glu):
        if (em >= 1 and t1 < 1 and t2 < 1):
            if (t1t2 > 1 and (em - t1t2) <1 and (t1+(em-t2-t1))<1 and  (t2+(em-t1-t2))<1 ):
                if (ul < 1):
                    EMr.append(g)
                if (ul >=1):
                    ULr.append(g)

    return EMr , ULr

# Extract the best and second best rValue of each points, plus it return a dctionary for each best txName
# with the information of the gluino, neutralino and rValue values
# NB: con False stai togliendo tutti quelli che hanno MAX >1,
# ma in questo modo stai togliendo anche quelli che hanno anche il resto, magari, > 1.
# pertanto quelli che rimangono (circa 2760 punti per Higgsino )
# sono meno di quelli che leggi dalla somma della legenda nel plot distribution vs gluino mass
# Se invece chiedi MAX > 1 and (sum - MAX) < 1 dovresti riotterere quell'altra
# scelgo questa cosi e' consistent con laltro grafico e piu facile da spiegare e connettere
def Extract_Best_txNames(Recast_Results,txNAMES = '', alsoSingle = True, exclusiveDoublets = False):
    
    Data_Lists = [] # rValues to be read
    Dics_Res = {} # Dics of results for the best txNames
    for name in txNAMES:
        Data_Lists.append(Recast_Results[name]['rValues']) # I append the lists of rValues
        NAME = name
        #dic = {NAME+'_Glu':[] , NAME+'_Neu':[], NAME+'_r':[]  }  # Creating the lists to be filled
        Dics_Res[NAME+'_Best_Glu']     = []
        Dics_Res[NAME+'_Best_Neu']     = []
        Dics_Res[NAME+'_Best_Neu2']    = []
        Dics_Res[NAME+'_Best_Ch1']     = []
        Dics_Res[NAME+'_Best_Stop']    = []
        Dics_Res[NAME+'_Best_Sbot']    = []
        Dics_Res[NAME+'_Best_Light_S'] = []
        Dics_Res[NAME+'_Best_r']       = []

        Dics_Res[NAME+'_2ndBest_Glu']     = []
        Dics_Res[NAME+'_2ndBest_Neu']     = []
        Dics_Res[NAME+'_2ndBest_Neu2']    = []
        Dics_Res[NAME+'_2ndBest_Ch1']     = []
        Dics_Res[NAME+'_2ndBest_Stop']    = []
        Dics_Res[NAME+'_2ndBest_Sbot']    = []
        Dics_Res[NAME+'_2ndBest_Light_S'] = []
        Dics_Res[NAME+'_2ndBest_r']       = []
        
    Max , Second, EM_Tot, SLHA = [] , [] , [] , []
    
    #Extracting the data from the dictionary:
    # I loop over each txNames and put the rValue
    for num in range(0,len(Data_Lists[0])): # I loop over all the points in the results (i.e. lenght of each rValue lists)
        Temp_List = [] # each Temp_List is the list of rValues each txName
        for tx in Data_Lists:
            Temp_List.append(tx[num])
        MAX = max(Temp_List)
#print MAX , ' ', Temp_List
#       raw_input(' ')
        if  (sum(Temp_List) < 1): continue # I select only excluded points
        if  (alsoSingle == False):
             if (MAX > 1  and ( sum(Temp_List) - MAX ) < 1): continue   # set to FALSE to consider only points which are not excluded by the best txName

        SECOND_MAX = max(n for n in Temp_List if n!=MAX)

        MpS = MAX + SECOND_MAX
        TOT = sum(Temp_List)
        if exclusiveDoublets == True:
           if not (MpS > 1 and (TOT - MpS) <1 and (MAX+(TOT-MAX-SECOND_MAX))<1 and  (SECOND_MAX+(TOT-SECOND_MAX-MAX))<1 ): continue
#if SECOND_MAX > 1 : continue
#       if MpS < 1: continue
#       if (sum(Temp_List) - MpS) > 1 : continue  # This selectes ONLY the points exlcuded by doublets

        Max.append(MAX) , Second.append(SECOND_MAX) , EM_Tot.append(Recast_Results['Tot_EM'][num]) , SLHA.append(Recast_Results['SLHA'][num])

        INDEX = Temp_List.index(MAX) # Index of the MAX element in the list (I need it to extract the txName)
        TX = txNAMES[INDEX]      # txName correspodning to the max value extracted (i.e. the txNAme
        Neu, Glu, Neu2, r = Recast_Results['Neu'][num] , Recast_Results['Glu'][num] , Recast_Results['Neu2'][num], Recast_Results[TX]['rValues'][num]
        Stop, Sbot, Light_S , Ch1 = Recast_Results['Stop'][num], Recast_Results['Sbot'][num], Recast_Results['Light_S'][num], Recast_Results['Ch1'][num]
        
        Dics_Res[TX+'_Best_Neu'].append(Neu)
        Dics_Res[TX+'_Best_Glu'].append(Glu)
        Dics_Res[TX+'_Best_r'].append(str(r))
        Dics_Res[TX+'_Best_Neu2'].append(Neu2)
        Dics_Res[TX+'_Best_Stop'].append(Stop)
        Dics_Res[TX+'_Best_Sbot'].append(Sbot)
        Dics_Res[TX+'_Best_Light_S'].append(Light_S)
        Dics_Res[TX+'_Best_Ch1'].append(Ch1)

        INDEX_2ND = Temp_List.index(SECOND_MAX) # Index of the MAX element in the list (I need it to extract the txName)
        TX_2nd = txNAMES[INDEX_2ND]      # txName correspodning to the max value extracted
        r_2 = Recast_Results[TX_2nd]['rValues'][num] # The masses are the same
        
        Dics_Res[TX_2nd+'_2ndBest_Neu'].append(Neu)
        Dics_Res[TX_2nd+'_2ndBest_Glu'].append(Glu)
        Dics_Res[TX_2nd+'_2ndBest_r'].append(str(r))
        Dics_Res[TX_2nd+'_2ndBest_Neu2'].append(Neu2)
        Dics_Res[TX_2nd+'_2ndBest_Stop'].append(Stop)
        Dics_Res[TX_2nd+'_2ndBest_Sbot'].append(Sbot)
        Dics_Res[TX_2nd+'_2ndBest_Light_S'].append(Light_S)
        Dics_Res[TX_2nd+'_2ndBest_Ch1'].append(Ch1)

#print str(len(Max)) , ' ',  str(len(Second)) , ' ', str(len(EM_Tot))
    return  Max, Second, EM_Tot, SLHA, Dics_Res
'''
    {'SLHA': ['Bino_fixSlep//100042885.slha'], 'T5tttt-EM': {'rValues': [0]}, 'T1tttt-EM': {'rValues': [0]}, 'T1-EM': {'rValues': [0]}, 'T2tt-EM': {'rValues': [0]}, 'Neu': [584.111445], 'TChiWW-EM': {'rValues': [0]}, 'T2bb-EM': {'rValues': [0]}, 'T5bbbb-EM': {'rValues': [0]}, 'T5WWoff-EM': {'rValues': [0]}, 'TChiZZ-EM': {'rValues': [0]}, 'T5-EM': {'rValues': [0]}, 'T5WW-EM': {'rValues': [0]}, 'Tot_EM': [0], 'TChiWZ-EM': {'rValues': [0]}, 'T2-EM': {'rValues': [0]}, 'T1bbbb-EM': {'rValues': [0]}, 'Glu': [594.699912], 'T6bbWW-EM': {'rValues': [0]}, 'T5ZZ-EM': {'rValues': [0]}, 'UL': [-1], 'T1btbt-EM': {'rValues': [0]}}
    
    txNames_CMS = [ 'T1tttt-EM','T1-EM','T2-EM', 'T2bb-EM' , 'T2tt-EM' , 'T6bbWW-EM', 'T1btbt-EM' , 'T1bbbb-EM',
    'T5-EM', 'T5bbbb-EM', 'T5tttt-EM' , 'T5WW-EM', 'T5WWoff-EM', 'T5ZZ-EM', 'TChiWW-EM', 'TChiWZ-EM', 'TChiZZ-EM'  ]
    '''


# extracting the gluino masses for the points ONLY excluded by T2+T5+TGQ
def Excluded_By_T2_T5_TGQ_only(Dic_Lists):
    t2 = Dic_Lists['T2-EM']['rValues']
    t5 = Dic_Lists['T5-EM']['rValues']
    tgq = Dic_Lists['T3GQon-EM']['rValues']
    
    Tx_g, Tot_EM , Ul , Slha =  Dic_Lists['Glu'] , Dic_Lists['Tot_EM'] , Dic_Lists['UL'] , Dic_Lists['SLHA']




    Excluded_Only_EM = { 'T2-T5-T3GQon':[], 'Glu' : [] , 'SLHA':[] } # this is for comparing exclusion irrespectively if the point is excluded already by UL
    Excluded_Only_UL = { 'T2-T5-T3GQon':[], 'Glu' : [] , 'SLHA':[] } # here we do not consider points already excluded by UL results
    
    for T2, T5, TGQ,  glu, tot, ul, slha in zip(t2, t5, tgq, Tx_g, Tot_EM , Ul , Slha) :
        r = T2 + T5 + TGQ
        if (r > 1 and (tot - r) < 1 and T2 < 1 and T5 < 1 and TGQ < 1):
            Excluded_Only_EM['T2-T5-T3GQon'].append(r) ,  Excluded_Only_EM['Glu'].append(glu) , Excluded_Only_EM['SLHA'].append(slha)
        if (r > 1 and (tot - r) < 1 and ul < 1 and T2 < 1 and T5 < 1 and TGQ < 1): # UL UNCONSTRAINED !!!!
            Excluded_Only_UL['T2-T5-T3GQon'].append(r) ,  Excluded_Only_UL['Glu'].append(glu) , Excluded_Only_UL['SLHA'].append(slha)

    return Excluded_Only_EM , Excluded_Only_UL


























