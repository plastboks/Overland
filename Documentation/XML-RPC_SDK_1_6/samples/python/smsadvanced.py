import xmlrpclib
import binascii
import sys

host = sys.argv[1]
to = sys.argv[2]

action = 0x03
responseenabler = 0xff
messageid = 0x0003
repeat = 3
totype = "endpoint"
ledcontrol = 0x00
iconnumber = 0x02
colorcontrol = 0x02
setupspec = 0x00
alerttone = 0x01
alertpattern = 0x01
alertvolume = 0x01
alerttimeout = 0x05
displaytimeout = 0x05
display = "5678"
callback = "3000"

server = xmlrpclib.Server("http://" + host)

session = server.session_login("GW-DECT/admin", "ip6000")

server.endpoint_sms_advanced(session, action, responseenabler, messageid, repeat, totype, to, ledcontrol,
                             iconnumber, colorcontrol, setupspec, alerttone, alertpattern, alertvolume,
                             alerttimeout, displaytimeout, display, callback)

while True:
	events = server.session_receive(session, 60)
	for event in events:
		if event["type"] == "endpoint_release":
			print "Endpoint release " + str(event)
		elif event["type"] == "endpoint_sms_advanced":
			print "Endpoint SMS advanced " + str(event)
		else:
			print "Unknown event: " + str(event)

server.session_logout(session)

