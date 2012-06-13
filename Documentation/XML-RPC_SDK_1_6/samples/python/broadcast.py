import xmlrpclib
import sys

host = sys.argv[1]
display = "Hello World!"

server = xmlrpclib.Server("http://" + host)

session = server.session_login("GW-DECT/admin", "ip6000")

server.endpoint_broadcast(session, display)

events = server.session_receive(session, 60)
for event in events:
	if event["type"] == "endpoint_broadcast":
		print "Broadcast status " + str(event["status"])
	else:
		print "Unknown event: " + str(event)

server.session_logout(session)

