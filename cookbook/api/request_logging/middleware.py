import socket
import time

import logging
log = logging.getLogger(__name__)

class RequestLogMiddleware(object):
    def process_request(self, request):
        request.start_time = time.time()

    def process_response(self, request, response):
        
        log_data = {
            'request_method': request.method,
            'request_path': request.get_full_path(),
            #'request_body': request.body,

            'response_status': response.status_code,

            'run_time': time.time() - request.start_time,
        }
        # how to get response content without capturing HTML??
        
        log.debug(log_data)
        # save log_data in some way

        return response