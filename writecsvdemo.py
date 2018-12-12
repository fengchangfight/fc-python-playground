

import csv

inputfile = "/Users/xiefengchang/dev/synonymous.txt"
lineno=1

output="./real_train.csv"

with open(inputfile,'r+', encoding="utf-8") as f, open(output, mode='w', newline='',encoding='utf-8') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',',
                            quoting=csv.QUOTE_ALL)
    spamwriter.writerow(['id', 'qid1', 'qid2', 'question1', 'question2', 'is_duplicate'])

    for line in f:
        outline=""
        arr=line.split("\t\t")
        if(len(arr)!=2):
            print("Invalid input...")
            continue
        print(arr)

        outlinearr=[]
        outlinearr.append(str(lineno-1))
        outlinearr.append(str(2*lineno-1))
        outlinearr.append(str(2*lineno))
        outlinearr.append(arr[0].strip())
        outlinearr.append(arr[1].strip())
        outlinearr.append("1")

        spamwriter.writerow([s for s in outlinearr])

        lineno+=1

