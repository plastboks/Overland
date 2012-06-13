import xmlrpclib
import binascii

host = "localhost:1080"

server = xmlrpclib.Server("http://" + host)

print "List implemented methods:"
print server.system.listMethods()

print "\nPrint method help:"
print server.system.methodHelp("endpoint_call_setup")

print "\nPrint method signature:"
print server.system.methodSignature("endpoint_call_setup")

