import facebook
from django.http import HttpResponse

def index(request):
    """
    The main view for the site.
    @author Eric Conner
    """
    return HttpResponse("Hello World!")