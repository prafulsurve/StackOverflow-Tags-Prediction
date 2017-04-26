import csv
import MySQLdb

mydb = MySQLdb.connect(host='localhost', user='root', passwd='1234', db='tagpredict_db')
cursor = mydb.cursor()

csv_data = csv.reader(file('../Data/data/train0.csv'))
cursor.execute('DELETE FROM stackoverflow')
print 'TABLE DATA DELETED'
for row in csv_data:
    cursor.execute('INSERT INTO stackoverflow(id, \
          title, body, tags )' \
          'VALUES(%s, %s, %s, %s)',
          row)
#close the connection to the database.
mydb.commit()
cursor.close()
print "Done"
