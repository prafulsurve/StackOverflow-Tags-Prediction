
echo Create Tokenized files
python parse_csv.py
echo Collect Top Tags
python getlabels.py
echo Collect 500 samples for top 10 tags
echo python split_by_label.py
echo Applying Naive Bayes to tokenized file
echo Writing into output.txt
python nb.py > output.txt
