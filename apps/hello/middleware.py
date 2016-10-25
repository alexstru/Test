from .models import RequestContent


class RequestContentMiddleware(object):

    def process_response(self, request, response):
        '''  Log request info in DB '''
        if request.path == "/request/" and request.is_ajax():
            return response

        request_log = RequestContent(
          method=request.method,
          path=request.build_absolute_uri(),
          status_code=response.status_code,
        )
        request_log.save()
        return response
