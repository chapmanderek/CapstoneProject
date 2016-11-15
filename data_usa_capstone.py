import requests
import sqlite3

# create and open a new sql database to house data
sql_connection = sqlite3.connect('state_info.sqlite')
cur = sql_connection.cursor()
cur.execute('DROP TABLE StateInfo')
cur.execute('''CREATE TABLE StateInfo 
	(id INTEGER PRIMARY KEY, name TEXT UNIQUE, id_num INTEGER UNIQUE, avg_wage_2014 INTEGER)''')

# get only state name and IDs into the database
state_json = requests.get("https://api.datausa.io/attrs/geo/?sumlevel=state").json()
state_data = state_json['data']
for each_state in state_data:
	cur.execute('INSERT OR IGNORE INTO StateInfo (name, id_num) VALUES (?, ?)', (each_state[9], each_state[8]))
sql_connection.commit()

# put wage info for each state into the database
# wage headers': [u'year', u'geo', u'avg_wage']
wage_url = "http://api.datausa.io/api/?show=geo&sumlevel=state&required=avg_wage"
wage_json = requests.get(wage_url).json()

wage_data = wage_json['data']
for each in wage_data:
	cur.execute('UPDATE StateInfo SET avg_wage_2014 = ? WHERE id_num = ?', (each[2], each[1]))
	# print each[1], " : ", each[2]
sql_connection.commit()

cur.close()