a = open('SummaryBino_noHeavyHiggsExclusion.txt','r').readlines() 

out = open('Bino_old_excluded_CHECK.dat','w')
out.write('#Old Bino Exclusion\n')

for l in a[1:]:
 splitt = l.split(' ')
 slha = splitt[0]
 rUL = float(splitt[58])
 rEM = float(splitt[61])
 if rUL > 1.0001 or rEM > 1.0001:
        out.write(slha + '\n')

out.close()

