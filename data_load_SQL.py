import sqlite3
import json

# create and open a new sql database to house data
sql_connection = sqlite3.connect('state_info.sqlite')
cur = sql_connection.cursor()
cur.execute('DROP TABLE IF EXISTS StateInfo')
cur.execute('''CREATE TABLE StateInfo 
	(id INTEGER PRIMARY KEY, name TEXT UNIQUE, geo_tag TEXT UNIQUE, avg_wage_2014 INTEGER, avg_edu_2014 INTEGER, election_winner TEXT, elec_win_percent INTEGER)''')

# Load state ids into sql database
print "Loading State ID #s..."
counter = 0
state_handle = open("state_ids.txt")
for each_state in state_handle:
	each_state_parts = each_state.rstrip().split(":")
	counter += 1
	cur.execute('INSERT OR IGNORE INTO StateInfo (name, geo_tag) VALUES (?, ?)', (each_state_parts[0], str(each_state_parts[1])))
sql_connection.commit()
print "Loaded {0} state IDs".format(counter)

# Load wage data into sql database
print "Loading Wage Data"
counter = 0
wage_handle = open("wage_data.txt")
for each_wage in wage_handle:
	counter += 1
	each_wage_parts = each_wage.split(":")
	cur.execute('UPDATE StateInfo SET avg_wage_2014 = ? WHERE geo_tag=?', (each_wage_parts[1], each_wage_parts[0]))
sql_connection.commit()
wage_handle.close()
print "Loaded wage data for {0} states".format(counter)

# Load education data into sql database
print "Loading education data"
counter = 0
edu_data = open("edu_data.txt")
for each_edu in edu_data:
	counter += 1
	each_edu_parts = each_edu.split(":")
	cur.execute('UPDATE StateInfo SET avg_edu_2014 = ? WHERE geo_tag = ?', (each_edu_parts[1], each_edu_parts[0]))
sql_connection.commit()
edu_data.close()
print "Loaded edu data for {0} states".format(counter)



cur.close()








