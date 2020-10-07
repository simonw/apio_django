import time
import sys
import traceback
import requests 
import json
import threading
import django
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings


class ApioMiddleware(MiddlewareMixin):
	"""Collates performance variables 
	and exception data to be shared with owner"""
	
	def process_exception(self, request, exception):

		apio_url_exception = "https://apio.in/remote_data_exception"

		#collating exception data
		exception_data = {
			"path": request.environ["wsgi.url_scheme"] + "://" \
			+ request.environ["HTTP_HOST"] + request.get_full_path(),
			"exception": exception.__class__.__name__+ \
			": " + str(sys.exc_info()[1]),
			"traceback":traceback.format_exc(),
			"user": str(request.user),
			"ip_address": request.META.get("REMOTE_ADDR")
		}		
		
		if exception_data["path"] != apio_url_exception:
			#sending request on new thread
			t = threading.Thread(
				target=send_exception_data_request, 
				args=[exception_data])
			t.start()
		return None
    
	def process_request(self, request):
		request.start_timestamp = time.time()

	def process_response(self, request, response):
		"""Calculate response time"""
		apio_perf_data_url = "https://apio.in/remote_perf_data"
		response_timestamp = time.time()

		#collating perf data
		perf_data = {
			"request_timestamp": request.start_timestamp,
			"response_timestamp": response_timestamp,
			"response_code": response.status_code,
			"path": request.environ["wsgi.url_scheme"] + "://" \
				+ request.environ["HTTP_HOST"] + request.get_full_path(),
			"requester": str(request.user),
			"ip_address": request.META.get("REMOTE_ADDR")
			}
		if perf_data["path"] != apio_perf_data_url:
			# Sending request on another thread
			t = threading.Thread(
				target=send_perf_data_request, args=[perf_data])
			t.start()
		return response


def send_exception_data_request(exception_data):
	"""sends perf data to remote server"""
	apio_url_exception = "https://apio.in/remote_data_exception"
	headers = {"x-api-key": 
		settings.APIO_D["application_key"]
	}
	r = requests.post(apio_url_exception, 
			data=json.dumps(exception_data), 
			headers=headers)
	print(r)

def send_perf_data_request(perf_data):
	"""sends perf data to remote server"""
	apio_perf_data_url = "https://apio.in/remote_perf_data"
	headers = {"x-api-key": 
		settings.APIO_D["application_key"]
	}
	r = requests.post(apio_perf_data_url, 
	data=json.dumps(perf_data), 
	headers=headers)
	print(r)	

