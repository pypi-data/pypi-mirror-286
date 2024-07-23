from .endpoint import *


		

class ApiServer(object):
	"""docstring for ApiServer"""
	def __init__(self, url, description=None):
		super(ApiServer, self).__init__()
		self.url = url
		self.description = description


class Api(object):
	"""docstring for Api"""
	def __init__(self, server, *endpoints, title=None, version=None, description=None, **kwargs):
		super(Api, self).__init__()
		self.endpoints = {
			str(endpoint.path):endpoint.setApi(self) for endpoint in endpoints
		}

		self.metadata = {
			"title":title,
			"version":version,
			"description":description
		}

		if server is None:
			self.servers = []
		elif issubclass(type(server),ApiServer):
			self.servers = [server]
		else:
			self.servers = list(server)

		if len(self.servers) > 0:
			self.switch_server(0)

	def addServer(self, server, switch_to=True):
		self.servers.append(server)
		if switch_to:
			self.switch_server(len(self.servers)-1)

	def switch_server(self, n):
		self.current_server = self.servers[n]

	def __getitem__(self,name):
		return self.endpoints[name]









		