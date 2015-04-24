# _extract_connections.py partial

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