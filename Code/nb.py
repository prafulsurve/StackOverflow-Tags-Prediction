import json
import math
import MySQLdb

tokens = '../Data/tokenized_data.json'
f = open(tokens,'r')
data = json.load(f)
intermediate = json.load(open('../Data/intermediate/intermediate0.json','r'))
mydb = MySQLdb.connect(host='localhost', user='root', passwd='1234', db='tagpredict_db')

#generate count - dictionary of dictionaries. count[word][tag] stores the count of entries with word and tag in the corpus
testrows = []
exptags = []
alltags = []
actual_title = []
qid = []
count = {}
entry = 0
output = []
counter = 0
for row in data:
    #if entry < 1500:
    # uncomment above for full run
    # comment below line for full run
    if entry < 50:
        testrows.append(row["title"])
        exptags.append(row["tags"])
        entry += 1
        alltags.extend(row["tags"])
    else:
        break

for row in data:
    for inter_row in intermediate:
        if row["id"] == inter_row["id"]:
            actual_title.append(inter_row["title"])
            qid.append(inter_row["id"])
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
    print "--------------------------------------------"
    return predictedTags[-3:]

TP = 0
FN = 0
FP = 0
TN = 0
for i in range(len(testrows)):
    print "--------------------------------------------"
    print "Question ID: ", (qid[i])
    output.append({})
    output[counter].update({'id':qid[i]})
    print "Title: ", (actual_title[i])
    output[counter].update({'title':actual_title[i]})
    print "Expected Tags", (exptags[i])
    output[counter].update({'expected': exptags[i]})
    acttags = predict(testrows[i])
    output[counter].update({'predicted': acttags})
    counter += 1
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

cursor = mydb.cursor()
cursor.execute('DELETE FROM predictedtags')
print 'TABLE DATA DELETED'
for row in output:
    exp = ' '.join(row['expected']).encode('utf-8')
    pred = ' '.join(row['predicted']).encode('utf-8')
    ttl = ''.join(row['title']).encode('utf-8')
    cursor.execute("""INSERT INTO predictedtags (id, title, expected, predicted ) VALUES(%s, %s, %s, %s)""", (row['id'], ttl, exp, pred))
    exp = ""
    pred = ""
    ttl = ""
mydb.commit()
cursor.close()
print "Written to Database"
