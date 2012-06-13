import xmlrpclib
import binascii
import sys

host = sys.argv[1]
to = sys.argv[2]

callback = "3000"
display = "Enter name"

server = xmlrpclib.Server("http://" + host)

session = server.session_login("GW-DECT/admin", "ip6000")

call = server.endpoint_call_setup(session, to, callback, "Hello - press OK")

while True:
	events = server.session_receive(session, 60)
	for event in events:
		if event["type"] == "endpoint_call_accept" and event["call"] == call:
			print "Text call accepted"
			server.endpoint_call_prompt(session, call, display)
		elif event["type"] == "endpoint_call_prompt" and event["call"] == call:
			if event["errorcode"] == 0:
				print "You entered '" + event["text"] + "'"
				server.endpoint_call_display(session, call, callback, "You entered " + event["text"])
			else:
				print "Error code " + str(event["errorcode"])
		elif event["type"] == "endpoint_call_release" and event["call"] == call:
			print "Text call released"
		else:
			print "Unknown event: " + str(event)

server.session_logout(session)

