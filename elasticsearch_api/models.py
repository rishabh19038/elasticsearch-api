from django.http import JsonResponse

class Response():
    def __init__(self, status_code=200, message=None, data=None):
        self.status_code = status_code
        self.message = message
        self.data = data

    def get_obj(self):
        return JsonResponse({
            'status_code': self.status_code,
            'message': self.message,
            'data': self.data,
        })