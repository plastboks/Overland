import xmlrpclib
import httplib

class PersistTransport(xmlrpclib.Transport):
	connection = None

	def request(self, host, handler, request_body, verbose=0):
		if not self.connection:
			host, extra_headers, x509 = self.get_host_info(host)
			self.connection = httplib.HTTPSConnection(host)
			self.headers = {"User-Agent" : self.user_agent, "Content-Type" : "text/xml", "Accept": "text/xml"}
			if extra_headers:
				for key, item in extra_headers:
					self.headers[key] = item

		self.headers["Content-Length"] = str(len(request_body))
		self.connection.request("POST", handler, request_body, self.headers)
		r = self.connection.getresponse()
		if r.status != 200:
			self.connection.close()
			self.connection = None
			raise xmlrpclib.ProtocolError( host + handler, r.status, r.reason, "")
		data = r.read()
		p, u = self.getparser()
		p.feed(data)
		p.close()
		return u.close()

host = "172.29.198.51"
to = "2632"
callback = "3000"
display = "Hello World!"

server = xmlrpclib.Server("https://" + host, transport = PersistTransport())

session = server.session_login("GW-DECT/admin", "ip6000")

server.endpoint_sms(session, to, callback, display)

server.session_logout(session)

