# 3rd party libs
import facebook

# Django utils
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

# Settings and local imports
from django.conf import settings

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
