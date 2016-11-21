import sqlite3
import json

# create and open a new sql database to house data
sql_connection = sqlite3.connect('state_info.sqlite')
cur = sql_connection.cursor()
cur.execute('DROP TABLE IF EXISTS StateInfo')
cur.execute('''CREATE TABLE StateInfo 
	(id INTEGER PRIMARY KEY, name TEXT UNIQUE, id_num INTEGER UNIQUE, avg_wage_2014 INTEGER)''')

# Load state ids into sql database
print "Loading State ID #s..."
counter = 0
state_handle = open("state_ids.txt")
for each_state in state_handle:
	each_state_parts = each_state.split(":")
	counter += 1
	cur.execute('INSERT OR IGNORE INTO StateInfo (name, id_num) VALUES (?, ?)', (each_state_parts[0], each_state_parts[1]))
sql_connection.commit()
print "Loaded {0} state IDs".format(counter)

# Load wage data into sql database
print "Loading Wage Data"
counter = 0
wage_data = open("wage_data.txt")
for each_wage in wage_data:
	counter += 1
	each_wage_parts = each_wage.split(":")
	cur.execute('UPDATE StateInfo SET avg_wage_2014 = ? WHERE id_num = ?', (each_wage_parts[2], each_wage_parts[1]))
sql_connection.commit()
print "Loaded  wage data for {0} states".format(counter)

cur.close()