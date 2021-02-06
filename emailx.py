import sqlite3

import requests

file = requests.get('https://www.py4e.com/code3/mbox.txt')

conn = sqlite3.connect('emaildb.sqlite')
cur = conn.cursor()
# print(file.text)
fh = open('email-txt.txt', mode='w+')
fh.writelines(file.text)
fh.close()

cur.execute('DROP TABLE IF EXISTS Counts')

cur.execute('''CREATE TABLE Counts (org TEXT, count INTEGER)''')

# fname = input('Enter file name: ')
# if (len(fname) < 1): fname = 'mbox-short.txt'
fh = open('email-txt.txt')
for line in fh.readlines():
    if not line.startswith('From: '): continue
    pieces = line.split()
    email = pieces[1]
    org = email.split(sep='@')[1]
    cur.execute('SELECT count FROM Counts WHERE org = ? ', (org,))
    row = cur.fetchone()
    if row is None:
        cur.execute('''INSERT INTO Counts (org, count)
                VALUES (?, 1)''', (org,))
    else:
        cur.execute('UPDATE Counts SET count = count + 1 WHERE org = ?',
                    (org,))
    conn.commit()

# # https://www.sqlite.org/lang_select.html
# sqlstr = 'SELECT email, count FROM Counts ORDER BY count DESC LIMIT 10'
#
# for row in cur.execute(sqlstr):
#     print(str(row[0]), row[1])

cur.close()
