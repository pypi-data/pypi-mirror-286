from temod.base.attribute import *

from .endpoint import *
from .api import *

import logging
import yaml


DEFAULT_PARSER = "3.0.0"


class SwaggerYmlParser(object):
	"""docstring for SwaggerYmlParser"""
	def __init__(self):
		super(SwaggerYmlParser, self).__init__()

	def parse(file,version=None):
		with open(file) as stream:
			dct = yaml.safe_load(stream.read())

		swagger_version = version if version is not None else dct.get('openapi',None)
		if swagger_version is None:
			logger.warn(f"No version properly identified, default parser for openapi version {DEFAULT_PARSER} have been selected")
			swagger_version = DEFAULT_PARSER

		return PARSERS[swagger_version]().load_api(dct)
		


class SwaggerYmlParser_3_0_0(object):
	"""docstring for SwaggerYmlParser_3_0_0"""

	ATTRIBUTES_CONSTRAINTS = {
		IntegerAttribute: {
			"default":"default_value",
			"minimum":"min",
			"maximum":"max",
			"format":None
		},
		StringAttribute: {
			"default":"default_value"
		},
		EnumAttribute: {
			"default":"default_value"
		},
		RangeAttribute: {
			"default":"default_value"
		}
	}

	def __init__(self):
		super(SwaggerYmlParser_3_0_0, self).__init__()

	def translate_schema(self, schema):
		attr_type = schema.get('type',"string")
		if attr_type == "string":
			values = schema.get('enum',None)
			if values is not None:
				dct = {"type":EnumAttribute, "values":list(values)}
			else:
				dct = {"type":StringAttribute}
		elif attr_type == "integer":
			values = schema.get('enum',None)
			if values is not None:
				dct = {"type":RangeAttribute, "values":list(values)}
			else:
				dct = {"type":IntegerAttribute}
		else:
			raise Exception(f"Undefined schema type: {schema['type']} (Not implemented yet)")

		for k,v in schema.items():
			if k in ['type', "enum"]:
				continue
			if not (k in SwaggerYmlParser_3_0_0.ATTRIBUTES_CONSTRAINTS[dct['type']]):
				raise Exception(f"Unknown constraint '{k}' for schema type '{schema['type']}' (Not implemented yet)")
			constraint = SwaggerYmlParser_3_0_0.ATTRIBUTES_CONSTRAINTS[dct['type']][k]
			if constraint is not None:
				dct[constraint] = v
		return dct

	def load_method(self, path, method, definition):
		headers = {}
		query = {}

		for parameter in definition.get('parameters',[]):
			location = parameter.get('in','query') 
			
			if location == "path":
				segment = path.getConfigurableSegment(parameter['name'])
				if segment is None:
					raise ParsingError(f"No parameter with name '{parameter['name']}' found in path {str(path)} (method: {method})")
				segment.description = parameter.get('description',segment.description)
				segment.constraints.update(self.translate_schema(parameter.get('schema',None)))

			elif location == "header":
				headers[parameter['name']] = Header(
					parameter['name'],value="{"+parameter['name']+"}",**self.translate_schema(parameter.get('schema',{}))
				)

			elif location == "cookie":
				raise Exception("Not implemented yet")

			elif location == "query":
				query[parameter['name']] = self.translate_schema(parameter.get('schema',None))

		return Method(
			METHODS[method], 
			summary=definition.get('summary'), 
			description=definition.get('description'),
			headers=headers,
			**query
		)

	def load_endpoint(self, path, definition):
		endpoint_path = Path.from_string(path)
		methods = [self.load_method(endpoint_path, method, params) for method, params in definition.items()]
		return Endpoint(endpoint_path, *methods)

	def load_server(self, definition):
		return ApiServer(**definition)

	def load_api(self, dct):
		swagger_version = dct.get('openapi','3.0.0')
		if swagger_version != "3.0.0":
			logging.warn("The version of the swagger implementation is not compatible with this parser andmay cause issues.")

		endpoints = [self.load_endpoint(path, endpoint) for path,endpoint in dct.get('paths',{}).items()]
		servers = [self.load_server(server) for server in dct.get('servers',[])]
		return Api(servers,*endpoints,**dct.get('infos',{}))

	def parse(self,file):
		with open(file) as stream:
			dct = yaml.safe_load(stream.read())

		return self.load_api(dct)
		


PARSERS = {
	"3.0.0":SwaggerYmlParser_3_0_0
}