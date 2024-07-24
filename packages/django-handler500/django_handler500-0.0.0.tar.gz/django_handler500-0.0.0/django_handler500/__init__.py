import sys

from django.views.debug import technical_500_response
from django.views.defaults import server_error

def handler500(request):
    if request.user.is_superuser:
        return technical_500_response(request, *sys.exc_info())
    template_name = os.getenv('DJANGO_HANDLER500_TEMPLATE_NAME','500.html')
    return server_error(request,template_name)
