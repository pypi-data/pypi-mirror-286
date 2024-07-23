from requests import Response

import requests
import logging


class BinaryResponse:
	"""docstring for BinaryResponse"""
	def __init__(self, response):
		super(BinaryResponse, self).__init__()
		self.value = response.content
		self.response = response

	def get(url, *args, **kwargs):
		print(f"GET Request to: {url}")
		return BinaryResponse(requests.get(url, *args,**kwargs))

	def post(url, *args, **kwargs):
		logging.info(f"POST Request to: {url}")
		return BinaryResponse(requests.post(url, *args,**kwargs))

	def put(url, *args, **kwargs):
		logging.info(f"PUT Request to: {url}")
		return BinaryResponse(requests.put(url, *args,**kwargs))

	def delete(url, *args, **kwargs):
		logging.info(f"DELETE Request to: {url}")
		return BinaryResponse(requests.delete(url, *args,**kwargs))

	def options(url, *args, **kwargs):
		logging.info(f"OPTIONS Request to: {url}")
		return BinaryResponse(requests.options(url, *args,**kwargs))

	def head(url, *args, **kwargs):
		logging.info(f"HEAD Request to: {url}")
		return BinaryResponse(requests.head(url, *args,**kwargs))

	def __getattribute__(self, name):
		try:
			return super(BinaryResponse,self).__getattribute__(name)
		except:
			return getattr(self.response,name)