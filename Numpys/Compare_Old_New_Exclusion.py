import os,sys
import numpy as np
import argparse


parser = argparse.ArgumentParser(description='Bino or Higgsino' )
parser.add_argument('--what',  '-W', help='Bino or Higgsino'    )

args      = parser.parse_args()
WHAT     = args.what


slha_old = np.load('Numpys_All/Old_Excluded_'+ WHAT +'.npy').item()['SLHA']
new      = np.load('Numpys_All/Excluded_ALL_'+ WHAT +'.npy').item()['SLHA']
slha_new  = [name.replace('.slha','') for name in new ]

not_now_but_before = list(set(slha_old) - set(slha_new)) # points that are not excluded now anymore
not_before_but_now = list(set(slha_new) - set(slha_old)) # points that can be excluded now but not before

print 'Excluded NOW', len(slha_new)
print 'Excluded BEFORE', len(slha_old)
print ' points that are not excluded now anymore ' , len(not_now_but_before)
print ' points that can be excluded now but not before ' , len(not_before_but_now)

miss = open('Missing_Points_' + WHAT + '.txt' , 'w')
miss.write('# Excluded before but not now' + WHAT + '\n')
for name in not_now_but_before:
    miss.write(name + '\n')

miss.close()


print not_before_but_now
improve = open('AdditionalExcludedNewPoints_' + WHAT + '.txt' , 'w')
improve.write('# Additionally Excluded Points with new TGQ maps ' + WHAT + '\n')
for name in not_before_but_now:
    improve.write(name + '\n')

improve.close()



