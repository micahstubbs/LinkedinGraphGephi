#! C:\python27\python
# encoding: utf-8

"""
linkedin-3-get_ids.py 

get a list of LinkedIn IDs for your 1st degree connections.

get this list after you retrieve your mutual connections 
and you will be able to find changes to your 1st degree connections list
that may have occured during the multiple days required to retrieve 
all mutual connections for networks larger than 400 first degree connections
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

start = 0 # Starting location within the result set for paginated returns. Ranges are specified with a starting index and a number of results (count) to return. 

filename_ids = "linked_ids_total.csv" %

def firstDegreeConnections():
	# Use your credentials to build the oauth client
	consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
	token = oauth.Token(key=OAUTH_TOKEN, secret=OAUTH_TOKEN_SECRET)
	client = oauth.Client(consumer, token)

	# Fetch first degree connections 
	v = "https://api.linkedin.com/v1/people/~/connections?format=json&start=%s" % start
	resp, content = client.request(v) 
	results = json.loads(content)

	# File that will store the results
	output_ids = codecs.open(filename_ids, 'w', 'utf-8')

	# Loop thru the 1st degree connections and get the ID 
	for result in results.get("values", "NA"):

		resultId = result["id"]
		con = "%s %s" % (result["firstName"].replace(",", " "), result["lastName"].replace(",", " "))

		print >>output_ids, "%s,%s" % (con, resultId)
		print "%s,%s" % (con, resultId)

if __name__ == '__main__':
	firstDegreeConnections()