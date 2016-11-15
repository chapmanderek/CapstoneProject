import requests



# get only state name and IDs into the database
print "Fetching State ID #s"
state_json = requests.get("https://api.datausa.io/attrs/geo/?sumlevel=state").json()
state_data = state_json['data']
counter = 0
state_id_dict = dict()
for each_state in state_data:
	counter += 1
	state_id_dict[each_state[9]] = each_state[8]

state_id_file = open("state_id_file.txt", 'w')
state_id_file.write(str(state_id_dict))
print "Fetched {0} state IDs".format(counter)


# put wage info for each state into the database
# wage headers': [u'year', u'geo', u'avg_wage']
wage_url = "http://api.datausa.io/api/?show=geo&sumlevel=state&required=avg_wage"
wage_json = requests.get(wage_url).json()

wage_data = wage_json['data']
