from django.http import HttpResponse
import json

def makeHttpResponse(data, status):
    response = HttpResponse(json.dumps(data), content_type="application/json", status=status)
    response['Cache-Control'] = 'max-age=0 no-cache, no-store, must-revalidate, private'
    response['Pragma'] = 'no-cache'
    response['Expires'] = 0
    response['X-XSS-Protection'] = 1
    return response
