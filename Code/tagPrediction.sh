
##############################
# Pre-processing data
# Generates intermediate/intermediate0.json and tokenized/tokenized0.json
##############################
echo "Create Tokenized files"
echo "-----------------------"
python parse_csv.py
echo " "
#
#
##############################
# Create map of labels and frequency
# Generates all_labels.json //TOP TAGS
##############################
echo "Collect Top Tags"
echo "-----------------"
python getlabels.py
echo " "
#
#
## Get 500 data points for top 10 labels
echo "Collect 500 samples for top 10 tags"
echo "------------------------------------"
python split_by_label.py
echo " "
#
#
# Call naive Bayes on the tokenized data
echo "Applying Naive Bayes to tokenized file"
echo "--------------------------------------"
python nb.py
echo " "
