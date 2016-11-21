import requests

# get only state name and IDs into the database
print "Fetching State ID #s..."
state_json = requests.get("https://api.datausa.io/attrs/geo/?sumlevel=state").json()
state_data = state_json['data']
counter = 0
state_id_file = open("state_ids.txt", 'w')
next_line = ""
for each_state in state_data:
	counter += 1
	next_line = each_state[9] + ":" + each_state[8] + "\n"
	state_id_file.write(next_line)
state_id_file.close()
print "Retrieved {0} state IDs".format(counter)

# put wage info for each state into the database
# wage headers': [u'year', u'geo', u'avg_wage']
print "Fetching wage data..."
wage_url = "http://api.datausa.io/api/?show=geo&sumlevel=state&required=avg_wage"
wage_json = requests.get(wage_url).json()
wage_data = wage_json['data']

wage_counter = 0
wage_data_file = open("wage_data.txt", 'w')
for each_state_wage in wage_data:
	wage_counter += 1
	next_line = each_state_wage[1] + ":" + str(each_state_wage[2]) + '\n'
	wage_data_file.write(next_line)
wage_data_file.close()
print "Retrieved {0} records of wage data".format(wage_counter)

# put education info for each state into the database
# wage headers': [u'year', u'geo', u'% people with some college']
print "Fetching education data..."
edu_url = "https://api.datausa.io/api/?show=geo&sumlevel=state&required=some_college"
edu_json = requests.get(edu_url).json()
edu_data = edu_json['data']

edu_counter = 0
edu_data_file = open("edu_data.txt", 'w')
for each_state_edu in edu_data:
	if each_state_edu[0] != 2015 : continue
	edu_counter += 1
	next_line = each_state_edu[1] + ':' + str(each_state_edu[2]) + '\n'
	edu_data_file.write(next_line)
print "Retrieved {0} records of edu data".format(edu_counter)
