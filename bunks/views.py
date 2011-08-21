import facebook
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

def index(request):
    """
    The main view for the site.
    @author Eric Conner
    """
    return render_to_response(
        "index.html", 
        {
            "bunks":[1,2,3],
        },
        context_instance = RequestContext(request)
    )