import xmlrpclib
import binascii
import sys

host = "172.17.13.96"

server = xmlrpclib.Server("https://" + host)
session = server.session_login("GW-DECT/admin", "kws8000")

server.endpoint_status(session, 1102, 0x19)

events = server.session_receive(session, 60)
for event in events:
	if event["type"] == "endpoint_status":
		print "Status " + str(event["status"]) + " 0x" + binascii.hexlify(event["data"].data) + " from " + event["from"]
	else:
		print "Unknown event: " + str(event)

server.session_logout(session)

