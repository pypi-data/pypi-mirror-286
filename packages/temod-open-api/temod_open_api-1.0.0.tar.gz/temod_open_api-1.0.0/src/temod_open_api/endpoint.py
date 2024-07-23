from temod.base.attribute import *

from .exceptions import *
from .response import *

from string import Formatter
from enum import Enum

import re


METHODS = Enum("METHODS",["get","post","put","patch","delete","head","options","trace","connect"])



def attributeFromConstraints(constraints, value=None):
	return self.constraints.get("type",StringAttribute)("placeholder",value=value,**{
		k:v for k,v in self.constraints.items() if not k in ["type","required"]
	})



class Segment(object):
	"""docstring for Segment"""
	def __init__(self, name: str, configurable=None, value=None, description=None, **kwargs):
		super(Segment, self).__init__()
		self.name = str(name)
		self.value = value
		self.description = description

		if not(configurable is False) and len(self.name) > 3 and self.name[0] == '{' and self.name[-1] == '}':
			self.is_parameter = True
			self.name = name[1:-1]
		else:
			self.is_parameter = False

		if not self.is_parameter and not Segment.isValid(self.name):
			raise UnallowedPathCharacter(f"Unallowed character in segment: {self.name}")

		self.constraints = kwargs

	def _setConstraints(self, constraints):
		self.constraints = constraints
		return self

	def validate(self):
		if len(self.constraints) > 0:
			try:
				attribute = attributeFromConstraints(self.constraints, value=self.value)
				if self.value is None:
					self.value = attribute.default_value
			except:
				raise InvalidParameterValue(f"Invalid value {self.value} for parameter {self.name}")
		return self

	def isEmpty(self):
		return self.name == ""

	def __call__(self,value):
		if not self.is_parameter:
			raise StaticSegmentError(f"The segment {self.name} is not configurable")
		return Segment(self.name,configurable=False,value=value)._setConstraints(self.constraints).validate()

	def __str__(self):
		return self.value if self.value is not None else self.name

	@staticmethod
	def isValid(name):
		# Define the allowed characters based on RFC 3986
		allowed_chars = re.compile(
			r'^[A-Za-z0-9\-._~!$&\'()*+,;=:@%]*$'
		)

		# Check if the name matches the allowed characters
		return bool(allowed_chars.match(name))


class Path(object):
	"""docstring for Path"""
	def __init__(self, *segments, is_root=True, remove_empty_segments=True):
		super(Path, self).__init__()

		self.is_root = is_root
		self.remove_empty_segments = remove_empty_segments

		self.segments = []
		for segment in segments:
			s = segment if issubclass(type(segment),Segment) else Segment(segment)
			if not s.isEmpty() or not remove_empty_segments:
				self.segments.append(s)

		self.parameters = [segment for segment in self.segments if segment.is_parameter]
		if len(set([segment.name for segment in self.parameters])) != len(self.parameters):
			raise DuplicatedParamName("Parameter names must be unique per path")

	def getSegment(self, name):
		for segment in self.segments:
			if segment.name == name:
				return segment

	def getConfigurableSegment(self, parameter_name):
		for segment in self.segments:
			if not segment.is_parameter:
				continue
			if segment.name == parameter_name:
				return segment

	def __call__(self, *args, **kwargs):
		segments = []
		arg_num = 0
		for segment in self.segments:
			if not segment.is_parameter:
				segments.append(segment)
				continue

			if segment.name in kwargs:
				segments.append(segment(kwargs.pop(segment.name)))
			else:
				try:
					segments.append(segment(args[arg_num]))
					arg_num += 1
				except IndexError:
					raise MissingParameter(f"The parameter {segment.name} is missing")

		return Path(*segments, is_root=self.is_root, remove_empty_segments=self.remove_empty_segments)

	def __str__(self):
		return (("/" if self.is_root else "")+("/".join([str(segment) for segment in self.segments])))

	@staticmethod
	def from_string(string, is_root=False,remove_empty_segments=True):
		print("Parsing path from string",string)
		segments = string.split("/")
		if segments[0] == "":
			segments = segments[1:]
			is_root = True
		print("Segments",segments, "is_root", is_root)
		return Path(*segments, is_root=is_root,remove_empty_segments=remove_empty_segments)
 

class Header(object):
	"""docstring for Header"""
	def __init__(self, key, value=None, is_parameter=None, **kwargs):
		super(Header, self).__init__()
		self.key = key
		self.value = value
		self.is_parameter = (self.value is None) or is_parameter

		self.parameter_names = []
		if not (self.is_parameter is False) and self.value is not None:
			self.is_parameter = self.extractParameters()

		self.constraints = kwargs

	def extractParameters(self):
		try:
			self.parameter_names = [i[1] for i in Formatter().parse(self.value) if i[1] is not None]
		except:
			self.parameter_names = []

		if "" in self.parameter_names:
			raise InvalidParameterName("Header value parameters must have a name")
		return len(self.parameter_names) > 0

	def validate(self):
		if len(self.constraints) > 0:

			try:
				attribute = attributeFromConstraints(self.constraints, value=self.value)
				if self.value is None:
					self.value = attribute.default_value
			except:
				raise InvalidParameterValue(f"Invalid value {self.value} for parameter {self.name}")

		return self

	def __call__(self, *value, **kwargs):
		if not self.is_parameter:
			return self.value

		if len(value) == 1:
			if self.value is None:
				return value
			else:
				return self.value.format(value)
		elif len(value) > 1:
			if self.value is None:
				raise TooManyParameters("Too many parameters where given")
			else:
				return self.value.format(*value)

		return self.value.format(**{k:v for k,v in kwargs.items() if k in self.parameter_names})
		

class Method(object):
	"""docstring for Method"""
	def __init__(self, method, summary=None, description=None, response=None, headers=None, **parameters):
		super(Method, self).__init__()

		self.method = method
		self.summary = summary
		self.headers = [] if headers is None else list(headers)
		self.response = response
		self.description = description
		self.parameters = parameters
		self.endpoint = None

	def setEndpoint(self, endpoint):
		self.endpoint = endpoint
		return self

	def __call__(self, api, endpoint, *body, **kwargs):
		if len(body) > 1:
			raise MethodCallError("Maximum one positionnal argument is allowed corresponding to the request body")

		if endpoint is None:
			endpoint = self.endpoint

		if api is None:
			api = endpoint.api

		data = body[0] if len(body) == 1 else None

		if self.response is None:
			response_type = BinaryResponse
		else:
			response_type = self.response

		headers = {header.key: header(kwargs) for header in self.headers}
		query = {
			parameter:attributeFromConstraints(constraints,value=kwargs.get(parameter)).value
			for parameter,constraints in self.parameters.items()
		}

		for k,v in kwargs.items():
			if k in self.parameters:
				continue
			additionnal = True
			for header in headers:
				if k in header.parameter_names:
					additionnal = False
					break
			if additionnal:
				query[k] = v

		return getattr(response_type,self.method.name)(
			Method.buildUrl(api, endpoint, **query),data=data,headers=headers
		)

	@staticmethod
	def buildUrl(api, endpoint, **query):
		if api.current_server is None:
			raise ServerNotFound("No api server selected to build url")
		query_str = "&".join([k+'='+str(v) for k,v in query.items()])
		query_str = f"?{query_str}" if len(query_str) > 0 else ''
		return f"{api.current_server.url}{str(endpoint.path)}{query_str}"



class Endpoint(object):
	"""docstring for Endpoint"""
	def __init__(self, path: Path, *methods, api=None):
		super(Endpoint, self).__init__()
		self.path = path
		self.methods = {
			method.method:method.setEndpoint(self) for method in methods
		}

		self.api = api

		if len(self.methods) != len(methods):
			_methods = [method.method for method in methods]
			raise DuplicatedMethod(
				f"Enpoint has multiple definitions for method: {[method for method in _methods if _methods.count(method) > 1][0]}"
			)

	def setApi(self, api):
		self.api = api
		return self

	def _setMethods(self, methods):
		self.methods = methods
		return self

	def __call__(self, *args, **kwargs):
		return Endpoint(self.path(*args,**kwargs), api=self.api)._setMethods(self.methods)

	def get(self,*args,**kwargs):
		try:
			method = self.methods[METHODS.get]
		except IndexError:
			raise MethodNotFound("Method 'get' was not associated with this endpoint")
		return method(self.api, self, *args,**kwargs)
		