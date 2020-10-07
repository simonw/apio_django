from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from sweetapi.helpers import SendEmail
import time
import sys
import traceback


class ExceptionMiddleware(MiddlewareMixin):
	def process_exception(self, request, exception):
		# SendEmail("error", "exception", ("nikhilmanahs@outlook.com",))
		print("Exception:", exception.__class__.__name__+ \
			": " + str(sys.exc_info()[1]))
		# print(request.__dict__)
		# print(request.environ)
		print("Path: ", request.environ["wsgi.url_scheme"] + "://" \
			+ request.environ["HTTP_HOST"] + request.get_full_path())
		print("Traceback: ", traceback.format_exc())
		# print(sys.exc_info()[2].__dict__)
		return HttpResponse("in exception")
        
	def process_request(self, request):
		request.start_time = time.time()
		# print (request.COOKIES)
		# print (request.user)
		# return print("bl")

	def process_response(self, request, response):
		"Calculate and output the page generation duration"
		# Get the start time from the request and calculate how long
		# the response took.
		duration = time.time() - request.start_time

		# Add the header.
		# response["X-Page-Generation-Duration-ms"] = int(duration * 1000)
		# print(response["X-Page-Generation-Duration-ms"])
		# return response
		return response

	# def process_response(self, request, response):
	# 	return print("ll")

	# def process_view(self, request):
	# 	return print("in papapapddddd v")
    
    

class StatsMiddleware(MiddlewareMixin):

    def process_request(self, request):
        "Store the start time when the request comes in."
        request.start_time = time.time()

    def process_response(self, request, response):
        "Calculate and output the page generation duration"
        # Get the start time from the request and calculate how long
        # the response took.
        duration = time.time() - request.start_time

        # Add the header.
        response["X-Page-Generation-Duration-ms"] = int(duration * 1000)
        print(response["X-Page-Generation-Duration-ms"])
        return response