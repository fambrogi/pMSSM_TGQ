
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

dire = '/scratch/fambrogi/PMSSM_TGQ/GitHub_Repo/pMSSM_TGQ/SLHA_LISTS/'

all                = [ name.replace('\n','') for name in open(dire + '/' + WHAT + '_LISTS_NOHEAVYHIGGS.txt' ,'r' ).readlines() ]
excluded_only_now  = [ name.replace('\n','') for name in open(dire + '/AdditionalExcludedNewPoints_' + WHAT + '.txt' ,'r' ).readlines() ]
exlcuded_before    = [ name.replace('\n','') for name in open(dire + '/' + WHAT +'_old_excluded.txt','r').readlines() ] 

print all
raw_input('')
print excluded_only_now
raw_input('')
print exlcuded_before
raw_input('')

print len(all) , len(excluded_only_now), len(exlcuded_before)


Still_not_excluded = list(set(all) - set(excluded_only_now) - set(exlcuded_before))

print 'Still not excluded: ', len(Still_not_excluded)

All_Excluded = excluded_only_now + exlcuded_before 
out = open('All_Excluded_Points_Before_plus_TGQ_' + WHAT + '.txt', 'w')
out.write('# All points excluded summing the old exclusion (published with Fastlim) and the new TGQ maps for ' + WHAT + '  \n')
for l in All_Excluded:
    out.write(l + '\n')

out.close()

Not_excluded = open('Still_Unexcluded_' + WHAT + '.txt', 'w')
Not_excluded.write('# All points STILL NOT excluded summing the old exclusion (published with Fastlim) and the new TGQ maps for ' + WHAT + '  \n')

for l in Still_not_excluded:
    Not_excluded.write(l + '\n')

Not_excluded.close()
