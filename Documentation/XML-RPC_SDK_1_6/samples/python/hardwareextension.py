import xmlrpclib
import binascii
import sys

host = sys.argv[1]
to = sys.argv[2]

hardwareelement = 0x01action = 0x01
repeat = 3
totype = "endpoint"
data = "0001"

server = xmlrpclib.Server("http://" + host)

session = server.session_login("GW-DECT/admin", "ip6000")

server.endpoint_hardware_extension(session, hardwareelement, action, repeat, totype, to, xmlrpclib.Binary(binascii.unhexlify(data)))

while True:
	events = server.session_receive(session, 60)
	for event in events:
		if event["type"] == "endpoint_hardware_extension":
			print "endpoint_hardware_extension " + str(event["element"]) + " " + str(event["reason"]) + " 0x" + binascii.hexlify(event["data"].data) + " from " + event["from"]
		else:
			print "Unknown event: " + str(event)

server.session_logout(session)

