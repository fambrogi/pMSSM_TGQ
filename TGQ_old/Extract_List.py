""" Extract the SLHA list of the points excluded by ATLAS
    and considered in outr previous work """

import os,sys

# select which dataset (Bino or Higgsino)
what = 'Higgsino'

# output file to be created
out = open(what + '_NoHiggs_SLHA.dat','w')

# old files (created by Ursula, can be found in the old Dropbox)

source = open('Summary'+what+'_noHeavyHiggsExclusion.txt','r').readlines()

for l in source[1:]:                                                      
    o = l.split(' ')[0]
    print o
    out.write( o + '\n')

          
print 'Total ' + what + ' : ' + str(len(source))
