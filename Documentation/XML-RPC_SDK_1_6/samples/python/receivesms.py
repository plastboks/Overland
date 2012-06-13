import xmlrpclib
import sys

host = sys.argv[1]

server = xmlrpclib.Server("http://" + host)

session = server.session_login("GW-DECT/admin", "ip6000")

while True:
	events = server.session_receive(session, 60)
	for event in events:
		if event["type"] == "endpoint_sms":
			print "SMS '" + event["display"] + "' to " + event["to"] + " from " + event["from"]
		else:
			print "Unknown event: " + str(event)

server.session_logout(session)

