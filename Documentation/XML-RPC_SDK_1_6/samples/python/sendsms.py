import xmlrpclib
import sys

host = sys.argv[1]
to = sys.argv[2]
callback = "3000"
display = "Hello World!"

server = xmlrpclib.Server("http://" + host)

session = server.session_login("GW-DECT/admin", "ip6000")

server.endpoint_sms(session, to, callback, display)

server.session_logout(session)

