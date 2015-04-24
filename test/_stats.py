# _stats.py partial

def stats(counter_GetConnectionProfile_APIcall, cap_GCP_APIcalls, relatedConnectionsTotal, mutualConnectionsStart, start):
	
	mutualConnectionsStart_next = mutualConnectionsStart + 20

	if counter_GetConnectionProfile_APIcall >= cap_GCP_APIcalls:
		print "API Call limit reached. %d call%s made to LinkedIn's Get Connection Profile API" % (counter_GetConnectionProfile_APIcall, "s"[counter_GetConnectionProfile_APIcall==1:])

		# All mutual connections have been retrieved for most recent person when API limit is reached
		if (relatedConnectionsTotal) <= (mutualConnectionsStart_next):
			z = counter_results
			next_start = start + z
			print "complete set of mutual connections retrieved for %d connection%s" % (z, "s"[z==1:])
			print "resume query at start = %d " % (next_start)
		
		# less than all of the mutual connections have been retrieved for most recent person when API limit is reached
		else:
			z = counter_results - 1
			next_start = start + z
			print "complete set of mutual connections retrieved for %d connection%s" % (z, "s"[z==1:])
			print "resume query at start = %d and mutualConnectionsStart = %d" % (next_start, mutualConnectionsStart_next)
		return

# all connections retrieved without reaching the API limit
def stats_end(counter_GetConnectionProfile_APIcall, counter_results):
	print "%d call%s made to LinkedIn's Get Connection Profile API" % (counter_GetConnectionProfile_APIcall, "s"[counter_GetConnectionProfile_APIcall==1:]) 
	z = counter_results
	print "mutual connections retrieved for %d connection%s" % (z, "s"[z==1:])


