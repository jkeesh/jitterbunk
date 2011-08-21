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
    # if not request.user.is_authenticated():
    #     return render_to_response(
    #         "login.html",
    #         {
    #             "facebook_app_id": settings.FACEBOOK_API_KEY
    #         },
    #         context_instance = RequestContext(request)
    #     )
    
    return render_to_response("index.html")