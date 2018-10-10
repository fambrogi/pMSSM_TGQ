# Extract the masses from the list of excluded points



a = open('SummaryBino_noHeavyHiggsExclusion.txt','r').readlines() 

out = open('Bino_old_excluded','w')
out.write('#Old Bino Exclusion')

for l in a[1:]:
 splitt = l.split(' ')
 slha = splitt[0]
 rUL = float(splitt[58])
 rEM = float(splitt[61])
 if rUL > 1.0001 or rEM > 1.0001:
        out.write(slha + '\n')
#        print 'Excluded!', rUL , ' ' , rEM
# else: print 'Not Excluded'

out.close()


a = open('SummaryBino_noHeavyHiggsExclusion.txt','r').readlines()

out = open('Higgsino_old_excluded','w')
out.write('#Old Bino Exclusion')

for l in a[1:]:
 splitt = l.split(' ')
 slha = splitt[0]
 rUL = float(splitt[58])
 rEM = float(splitt[61])
 if rUL > 1.0001 or rEM > 1.0001:
        out.write(slha + '\n')
#        print 'Excluded!', rUL , ' ' , rEM
# else: print 'Not Excluded'
out.close()



