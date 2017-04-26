import json
import os

# list of top ten tags
# already curated from data
top10 = {}
fin = open('../Data/all_labels.json','r')
d = json.load(fin)
for row in d:
    top10[row[0]] = row[1]
print top10


filepath = "../Data/tokenized/"
tokenpath = "../Data/tokenized_data.json"

max_lines = 500
feed = []

def split_by_label(data):
    for row in data:
        for label in top10.keys():
            if (top10[label]<max_lines):
                if label in row["tags"]:
                    feed.append(row)
                    top10[label] = top10[label] + 1
                    break

label_file = open(tokenpath,'w')
for dir, subdir, files in os.walk(filepath):
    for filename in files:
        f = os.path.join(dir,filename)
        if not all(value == max_lines for value in top10.values()):
            file = open(f,'r')
            data = json.load(file)
            split_by_label(data)
        else:
            break

print 'tokenized_data Length: ' + str(len(feed))
json.dump(feed,label_file)
label_file.close()
file.close()
