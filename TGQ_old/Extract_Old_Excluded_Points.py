a = open('SummaryBino_noHeavyHiggsExclusion.txt','r').readlines() 

out = open('Bino_old_excluded','r')
out.write('#Old Bino Exclusion')

for l in a[1:]:
 splitt = l.split(' ')
 slha = splitt[0]
 rUL = splitt[58]
 rEM = splitt[61]
 if rUL > 1.0001 or rEM > 1.0001:
        out.write(slha + '\n')

out.close()

