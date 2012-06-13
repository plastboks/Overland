import xmlrpclib
import binascii
import sys

host = sys.argv[1]

server = xmlrpclib.Server("http://" + host)

session = server.session_login("GW-DECT/admin", "ip6000")

while True:
	events = server.session_receive(session, 60)
	for event in events:
		if event["type"] == "endpoint_status":
			print "Status " + str(event["status"]) + " 0x" + binascii.hexlify(event["data"].data) + " from " + event["from"]
		else:
			print "Unknown event: " + str(event)

server.session_logout(session)

