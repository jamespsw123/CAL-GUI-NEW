import csv
RESULTS = [
    ['apple','cherry','orange','pineapple','strawberry']]
plus = ['1','2','2','2','5']
RESULTS.append(plus)
date = '07-24-2015'
filename = date+'.csv'
resultFile = open(filename,'wb') 
wr = csv.writer(resultFile, dialect='excel')
wr.writerows(RESULTS)