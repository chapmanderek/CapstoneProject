import sqlite3

# create and open a new sql database to house data
sql_connection = sqlite3.connect('state_info.sqlite')
cur = sql_connection.cursor()
cur.execute('DROP TABLE StateInfo')
cur.execute('''CREATE TABLE StateInfo 
	(id INTEGER PRIMARY KEY, name TEXT UNIQUE, id_num INTEGER UNIQUE, avg_wage_2014 INTEGER)''')

print "Loading State ID #s"
for each_state in state_data:
	cur.execute('INSERT OR IGNORE INTO StateInfo (name, id_num) VALUES (?, ?)', (each_state[9], each_state[8]))
sql_connection.commit()

print "Loading Wage Data"
for each in wage_data:
	cur.execute('UPDATE StateInfo SET avg_wage_2014 = ? WHERE id_num = ?', (each[2], each[1]))
	# print each[1], " : ", each[2]
sql_connection.commit()

cur.close()