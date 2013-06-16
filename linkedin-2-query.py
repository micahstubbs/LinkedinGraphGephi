#! C:\python27\python
# encoding: utf-8

"""

linkedin-2-query.py

inspired by Thomas Cabrol 

Building the LinkedIn Graph

"""

try:
    import json
except ImportError:
    import simplejson as json

import oauth2 as oauth 
import urlparse
import codecs

CONSUMER_KEY = "js6zocdd9j86"
CONSUMER_SECRET = "alkyBWF4yidK20sb"
OAUTH_TOKEN = "be8fa919-c03a-465b-b4b8-631cf4cd5eb9"
OAUTH_TOKEN_SECRET = "e939a72d-8b7b-4278-bc05-f27014c20db3"

start = 1101 # Starting location within the result set for paginated returns. Ranges are specified with a starting index and a number of results (count) to return. 
count = 500 #number of results to return. You may specify any number. Default and max page size is 500. Implement pagination to retrieve more than 500 connections.
#end = start + count - 1

# start + count = nextStart
# nextStart = 

filename = "linked_%s.csv" % start
filename_ids = "linked_ids_%s.csv" % start

def linkedin_connections():
	# Use your credentials to build the oauth client
	consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
	token = oauth.Token(key=OAUTH_TOKEN, secret=OAUTH_TOKEN_SECRET)
	client = oauth.Client(consumer, token)
	
	# daily limit per developer is 500 calls to the "People Search" API
	# http://developer.linkedin.com/documents/throttle-limits
	counter_GetConnectionProfile_APIcall = 0
	cap_GCP_APIcalls = 500

	# track how many connections been queried
	counter_results = 0

	# Fetch first degree connections 
	v = "https://api.linkedin.com/v1/people/~/connections?format=json&start=%s&count=%s" % (start, count)
	resp, content = client.request(v) 
	results = json.loads(content)
	
	# File that will store the results
	output = codecs.open(filename, 'w', 'utf-8')
	output_ids = codecs.open(filename_ids, 'w', 'utf-8')

	def extract_connections(rels, con):
		print '*'
		try:
			for rel in rels['relationToViewer']['relatedConnections']['values']:
				sec = "%s %s" % (rel["firstName"].replace(","," "), rel["lastName"].replace(",", " "))
				y = "%s,%s" % (con, sec)
				print y
				print >>output, y

		except:
			print "Exception encountered, exiting loop"
			pass
		print '*'

	# Loop thru the 1st degree connections and see how they connect to each other 
	for result in results.get("values", "NA"):

		resultId = result["id"]
		#resultId = 

		con = "%s %s" % (result["firstName"].replace(",", " "), result["lastName"].replace(",", " "))
		print >>output, "%s,%s" % ("Micah Stubbs", con)
		print "%s,%s" % ("Micah Stubbs", con)		
		print >>output_ids, "%s,%s" % (con, resultId)
		print "%s,%s" % (con, resultId)

		# This is the trick, use the search API to get related connections
		# gather first 20 mutual connections, and the total
		mutualConnectionsStart = 0
		relatedConnectionsTotal = 0

		u = "https://api.linkedin.com/v1/people/%s:(relation-to-viewer:(related-connections))?format=json&count=20&start=%s" % (resultId, mutualConnectionsStart)
		resp, content = client.request(u)
		counter_GetConnectionProfile_APIcall += 1
		rels = json.loads(content)
		
		try:
			relatedConnectionsTotal = int(rels['relationToViewer']['relatedConnections']['_total'])
			print relatedConnectionsTotal
			extract_connections(rels,con)

		except:
			print "Exception encountered, going to next connection"
			pass

		counter_results += 1

		if counter_GetConnectionProfile_APIcall >= cap_GCP_APIcalls:
			print "API Call limit reached. %d call%s made to LinkedIn's Get Connection Profile API" % (counter_GetConnectionProfile_APIcall, "s"[counter_GetConnectionProfile_APIcall==1:])

			if (relatedConnectionsTotal) > (mutualConnectionsStart):
				z = counter_results
			else:
				z = counter_results - 1 
					
			print "mutual connections retrieved for %d connection%s" % (z, "s"[z==1:])
			return


		# gather mutual connections 20 at a time, if the total is larger than the starting amount plus 20
		while (relatedConnectionsTotal - 1) > (mutualConnectionsStart + 20):
			mutualConnectionsStart += 20
			u = "https://api.linkedin.com/v1/people/%s:(relation-to-viewer:(related-connections))?format=json&count=20&start=%s" % (resultId, mutualConnectionsStart)
			resp, content = client.request(u)
			counter_GetConnectionProfile_APIcall += 1
			rels = json.loads(content)
			
			extract_connections(rels,con)

			if counter_GetConnectionProfile_APIcall >= cap_GCP_APIcalls:
				print "API Call limit reached. %d call%s made to LinkedIn's Get Connection Profile API" % (counter_GetConnectionProfile_APIcall, "s"[counter_GetConnectionProfile_APIcall==1:])

				if (relatedConnectionsTotal) > (mutualConnectionsStart):
					z = counter_results
				else:
					z = counter_results - 2 

				print "complete set of mutual connections retrieved for %d connection%s" % (z, "s"[z==1:])
				return

	# Print some stats to the console 
	print "%d call%s made to LinkedIn's Get Connection Profile API" % (counter_GetConnectionProfile_APIcall, "s"[counter_GetConnectionProfile_APIcall==1:]) 
	
	z = counter_results
	print "mutual connections retrieved for %d connection%s" % (z, "s"[z==1:])
		

if __name__ == '__main__':
		linkedin_connections()			
