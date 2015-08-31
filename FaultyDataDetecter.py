import urllib2
import json  # import this for json formatting  

def hellofun():
	response = urllib2.urlopen("https://www.test.jugnoo.in:8300/fetch_data")

	#temp = open('engagement_data.txt', 'r')
	html = response.read()
	res = []
	
	#print html;
	tmp = json.loads(html)   #encoding
	for k in tmp:
		loop_data = {}
		dis1 = k['metered_distance']
		tim1 = k['metered_time']
		url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins="+str(k["pickup_latitude"])+","+str(k["pickup_longitude"])+"&destinations="+str(k["drop_latitude"])+","+str(k["drop_longitude"])
		#print url
		#https://maps.googleapis.com/maps/api/distancematrix/json?origins=30.727539,76.754992&destinations=30.699249,76.784705&key=AIzaSyCjaXIg4FzJl_bG-uFzX9HcLMgEyfJvDoo
		
		#key=AIzaSyCjaXIg4FzJl_bG-uFzX9HcLMgEyfJvDoo
		response = urllib2.urlopen(url)
		htm = response.read()
		goog = json.loads(htm)
		x =  goog[u'rows']
		loop_data['engagement_id'] = k['engagement_id']
		loop_data['metered_distance'] = dis1
		loop_data['metered_time'] = tim1
		for q in x:
			#print q;
			#goog = json.loads(q)
			g = q[u'elements']
			for f in g:
				dis =  f['distance']['value']
				dur =  f['duration']['value']
				#print "engagement_id : " + str(k['engagement_id'])
				#print "metered_distance :" + str(dis1)
				#print "metered_time : " + str(tim1)
				#print "estimated goog dis in kms: "+ str(dis/1000)
				#print "estimated goog time in secs : "+ str(dur)
				dis_dev = abs(((dis/1000.0001)/(dis1+.01))*100 - 100)  # find dist_deviation
				time_dev = abs((dur/(tim1*60.0+.0001))*100 - 100)  # find time deviation

				#print dis_dev,time_dev   # print deviation

				loop_data['time_deviation'] = str(dis_dev)+"%"
				loop_data['distance_deviation'] = str(time_dev)+"%"

				
		if(dis_dev > 15 or time_dev > 20):   #  take any threshold  i took if distance error > 15 % or time error > 20 % then its faulty
			res.append(loop_data)   # put this set to res  

	res_data = json.dumps(res)  # decoding
	return res_data;  

print hellofun()   #  print all faulty sets in json format  
