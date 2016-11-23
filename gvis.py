import sqlite3
winner_percent_multiplier = 1.25
data = ''
sql_connection = sqlite3.connect('state_info.sqlite')
cur = sql_connection.cursor()
cur.execute('SELECT geo_tag FROM StateInfo')

#import data into array for chart
# get id tags to itterate through, stash in a list
geotags = cur.fetchall()

# for each state 
for each_tag in geotags:
	cur.execute('SELECT * FROM StateInfo WHERE geo_tag = ?', (each_tag[0], ))
	sdata = cur.fetchone()
	key, pname, pgeo_tag, pwage_data, pedu_data, pwinner, pwin_percent = sdata
	# statedata --> key, name, geo_tag, wage data, edu data, winner, winner percent
	# point_info [1, 4, \'point {size: 40; fill-color: #002DFF  }\'],
	if pwinner == 'Clinton' : pcolor = '#002DFF'
	elif pwinner == 'Trump' : pcolor = '#FF2D00'
	psize = (pwin_percent - 45.41) * winner_percent_multiplier
	
	# wage data --> x value; percent won --> point size; edu data --> y value; winner --> point color hillary #002DFF  trump  #FF2D00
	point_info = '[{x}, {y}, \'point {{size: {size}; fill-color: {color} }}\', \'{name}\'],'.format(name = pname, x = pwage_data, y = pedu_data, size= psize, color=pcolor)
	data = data + point_info + '\n'

data = data + ']);' + '\n'

beg_html = '<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script> \n <div id="chart_div" style="width: 1000px; height: 700px;"></div>' + '\n'
beg_js = '''<script>\ngoogle.charts.load('current', {'packages':['corechart']});\ngoogle.charts.setOnLoadCallback(drawChart);\nfunction drawChart() 
{var data = google.visualization.arrayToDataTable([['X', 'Y', {'type': 'string', 'role': 'style'}, {'type': 'string', 'role': 'tooltip'}],\n'''
# data in middle
js_options = '''var options = {legend: 'none', width: 900, height: 600, title: '2016 Election Results by State', 
				hAxis: { title: 'Avg Wage per Person', minValue: 40000, maxValue: 60000, gridlines: 8 },\nvAxis: { title: 'Amount of Education', minValue: .5, maxValue: .75 } };' + '\n'''
end_js = '''var chart = new\ngoogle.visualization.ScatterChart(document.getElementById(\'chart_div\'));\nchart.draw(data, options);\n}\n</script>\n'''
gvis_handle = open('gvis.html', 'w')
gvis_handle.write(beg_html)
gvis_handle.write(beg_js)
gvis_handle.write(data)
gvis_handle.write(js_options)
gvis_handle.write(end_js)

gvis_handle.close()