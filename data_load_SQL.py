import sqlite3
import json

# create and open a new sql database to house data
sql_connection = sqlite3.connect('state_info.sqlite')
cur = sql_connection.cursor()
cur.execute('DROP TABLE IF EXISTS StateInfo')
cur.execute('''CREATE TABLE StateInfo 
	(id INTEGER PRIMARY KEY, name TEXT UNIQUE, geo_tag TEXT UNIQUE, avg_wage_2014 INTEGER, avg_edu_2014 INTEGER, elec_winner TEXT, elec_win_percent INTEGER)''')

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

# Load election winner and data
# Columns = State,Hillary Clinton %,Donald Trump %  --> hillary % = 1, trump % = 2
elec_handle = open('ElectionResultsByState.csv')
counter = 0
for each_state_result in elec_handle:
	counter += 1
	winner = None
	winner_percent = 0
	each_state_result = each_state_result.replace('%', '')
	each_state_result_parts = each_state_result.rstrip().split(',')

	# determine who won
	if each_state_result_parts[1] > each_state_result_parts[2]:  #hillary won state
		winner = 'Clinton'
		winner_percent = each_state_result_parts[1]
	elif each_state_result_parts[2] > each_state_result_parts[1]:  #trump won state
		winner = 'Trump'
		winner_percent = each_state_result_parts[2]
	else : print "Error loading some states election info"
	cur.execute('UPDATE StateInfo SET elec_winner = ?, elec_win_percent = ? WHERE name = ?', (winner, winner_percent, each_state_result_parts[0]))
print "Loaded election data for {0} states".format(counter) 
sql_connection.commit()
elec_handle.close()

cur.close()








