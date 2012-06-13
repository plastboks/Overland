import xmlrpclib
import binascii
import datetime
import sys

host = sys.argv[1]
to = sys.argv[2]
callback = "3000"

server = xmlrpclib.Server("http://" + host)

session = server.session_login("GW-DECT/admin", "ip6000")

call = server.endpoint_call_setup(session, to, callback, "Hello - press OK", 0x0A, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, xmlrpclib.DateTime(datetime.datetime(2009, 4, 5, 1, 2, 0)))

while True:
	events = server.session_receive(session, 60)
	for event in events:
		if event["type"] == "endpoint_call_accept" and event["call"] == call:
			print "Text call accepted"
			server.endpoint_call_display(session, call, callback, "Thank you")
		elif event["type"] == "endpoint_call_key" and event["call"] == call:
			print "You pressed " + event["key"]
			server.endpoint_call_display(session, call, callback, "You pressed " + event["key"])
		elif event["type"] == "endpoint_call_release" and event["call"] == call:
			print "Text call released"
			call = None
		else:
			print "Unknown event: " + str(event)

server.session_logout(session)

