import json
import math

tokens = '../Data/tokenized_data.json'

f = open(tokens,'r')
data = json.load(f)

#generate count - dictionary of dictionaries. count[word][tag] stores the count of entries with word and tag in the corpus
testrows = []
exptags = []
alltags = []

count = {}
entry = 0
for row in data:
    #if entry < 1500:
    # uncomment above for full run
    # comment below line for full run
    if entry < 1525:
        testrows.append(row["title"])
        exptags.append(row["tags"])
        entry += 1
        alltags.extend(row["tags"])
    else:
        break

#data = data[1500:]
# uncomment above for full run
# comment below line for full run
data = data[10:]

for row in data:
    title = row["title"]
    alltags.extend(row["tags"])
    tags = row["tags"]
    for word in title:
        for tag in tags:
            if word not in count.keys():
                count[word] = {}
                count [word][tag] = 1
            else:
                if tag not in count[word].keys():
                    count[word][tag] = 1
                else:
                    count[word][tag] += 1

#get count of occurances of a tag across documents
docCount = {}
for row in data:
    tags = row["tags"]
    for tag in tags:
        if tag not in docCount.keys():
            docCount[tag] = 1
        else:
            docCount[tag] += 1


#doc = "file open C unable help"
#xspredict(doc)
def Pr(word, tag):
    numerator = 1
    if word in count.keys():
        if tag in count[word].keys():
            numerator += count[word][tag]

    denominator = 0;
    V = len(count.keys())
    for word in count.keys():
        if tag in count[word].keys():
            denominator += count[word][tag]
    return numerator*1.0/(denominator + V)

def Pr1(tag):
    totalDocs = len(data)
    return docCount[tag]*1.0/totalDocs

def bagofwords(doc):
    return doc

def perf(exp, pred):
    tp = len(exp.intersection(pred))
    fn = len(pred.difference(exp))
    fp = len(exp.difference(pred))
    tn = len((set(alltags)).difference(exp.union(pred)))
    return [tp, fn, fp, tn]

def predict(doc):
    e = {}
    doc = bagofwords(doc)
    tags = docCount.keys()
    for tag in tags:
        e[tag] = math.log(Pr1(tag))
        prod = 0.0
        for word in doc:
            prod += math.log(Pr(word, tag))
        e[tag] += prod

    #get key with max value in dictionary
    predictedTags = sorted(e, key=e.__getitem__)
    print "Predicted Tags", (predictedTags[-3:])
    return predictedTags[-3:]

TP = 0
FN = 0
FP = 0
TN = 0
for i in range(len(testrows)):
    print "Expected Tags", (exptags[i])
    acttags = predict(testrows[i])
    [tp, fn, fp, tn] = perf(set(exptags[i]), set(acttags))
    TP += tp
    FN += fn
    FP += fp
    TN += tn
    print

recall = TP*1.0/(TP+FN)
if TP==0 and FP==0:
    precision = 0
else:
    precision = TP*1.0/(TP+FP)

if recall==0 and precision==0:
    f1_score = 0
else:
    f1_score = 2.0*recall*precision/(recall+precision)

print "Performance summary"
print "Accuracy:", "\t", 1.0*(TP+TN)/(TP+FP+FN+TN)
print "Error:\t", 1.0*(FP+FN)/(TP+FP+FN+TN)
print "Recall:","\t",  1.0*TP/(TP+FN)
print "Precision:","\t",  1.0*TP/(TP+FP)
print "Specificity:","\t",  1.0*TN/(TN+FP)
print "F1 score:", "\t", f1_score
print
