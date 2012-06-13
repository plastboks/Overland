import xmlrpclib
import sys

host = sys.argv[1]
to = sys.argv[2]

server = xmlrpclib.Server("http://" + host)

session = server.session_login("GW-DECT/admin", "ip6000")

server.endpoint_base_stations(session, to)

events = server.session_receive(session, 60)
for event in events:
	if event["type"] == "endpoint_base_stations":
		for rfp in event["rfp_map"]:
			print str(rfp["rpn"]) + " - " + str(rfp["rssi"])
	else:
		print "Unknown event: " + str(event)

server.session_logout(session)

