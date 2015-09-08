import urllib2
import json  

def DetectFaultyData():
	response = urllib2.urlopen("https://www.test.jugnoo.in:8300/fetch_data")

	html = response.read()
	res = []

	JSONtoDict = json.loads(html)   #converting JSON into normal dictionary
	#print JSONtoDict
	for k in JSONtoDict:
		loop_data = {}

		loop_data['engagement_id'] = k['engagement_id']
		loop_data['metered_distance'] =  k['metered_distance']
		loop_data['metered_time'] = k['metered_time']
		#Getting estimated data from google API

		#https://maps.googleapis.com/maps/api/distancematrix/json?origins=30.727539,76.754992&destinations=30.699249,76.784705&key=AIzaSyCjaXIg4FzJl_bG-uFzX9HcLMgEyfJvDoo
		#key=AIzaSyCjaXIg4FzJl_bG-uFzX9HcLMgEyfJvDoo
		url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins="+str(k["pickup_latitude"])+","+str(k["pickup_longitude"])+"&destinations="+str(k["drop_latitude"])+","+str(k["drop_longitude"])
		
		response = urllib2.urlopen(url)
		TempHtmlData = response.read()
		TempDict = json.loads(TempHtmlData)

		RowCount =  TempDict[u'rows']
		
		dis1 = k['metered_distance']
		time1 = k['metered_time']

		for q in RowCount:
			#print q;
			#goog = json.loads(q)
			g = q[u'elements']
			for f in g:
				Estimated_dist =  f['distance']['value']  # estimated distance
				Estimated_dur =  f['duration']['value']   # estimated time
				# find dist_deviation
				dist_dev = abs(((Estimated_dist/1000.0001)/(dis1+.01))*100 - 100)  
				# find time deviation
				time_dev = abs((Estimated_dur/(time1*60.0+.0001))*100 - 100)  

				#print dis_dev,time_dev 

				loop_data['time_deviation'] = str(dist_dev)+"%"
				loop_data['distance_deviation'] = str(time_dev)+"%"

				
		if(dist_dev > 15 or time_dev > 20):   #  if distance error > 15 % or time error > 20 % then its faulty
			res.append(loop_data)   # put this set to result set  

	res_data = json.dumps(res)  # convert list pr dict to JSON
	return res_data  

print DetectFaultyData()   
