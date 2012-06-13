import xmlrpclib
import binascii
import sys
import socket
import time

hosts = list()
hosts.append(sys.argv[1])
hosts.append(sys.argv[2])

servers = list()
servers.append(xmlrpclib.Server("http://" + hosts[0]))
servers.append(xmlrpclib.Server("http://" + hosts[1]))

server = servers[0]
session = None

while True:
	try:
		if not session:
			print server
			session = server.session_login("GW-DECT/admin", "ip6000")
		events = server.session_receive(session, 60)
		for event in events:
			if event["type"] == "endpoint_status":
				print "Status " + str(event["status"]) + " 0x" + binascii.hexlify(event["data"].data) + " from " + event["from"]
			elif event["type"] == "endpoint_sms":
				print "SMS '" + event["display"] + "' to " + event["to"] + " from " + event["from"]
			else:
				print "Unknown event: " + str(event)
	except (xmlrpclib.ProtocolError, socket.error) as detail:
		print detail
		time.sleep(1)
		session = None
		if server is servers[0]:
			server = servers[1]
		else:
			server = servers[0]

server.session_logout(session)

