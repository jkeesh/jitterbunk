import facebook
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

def login(request):
    """
    Display a login page to the user.
    """
    return render_to_response(
        "login.html",
        {
            "facebook_app_id": settings.FACEBOOK_API_KEY
        },
        context_instance = RequestContext(request)
    )


def index(request):
    """
    The main view for the site.
    """
    return render_to_response(
        "index.html", 
        {
            "bunks":[1,2,3],
        },
        context_instance = RequestContext(request)
    )

def profile(request, id):
    """
    Display someone's profile page to the user.
    """
    return render_to_response("profile.html", {
        "viewer": request.user,
        "id": id,
        },
        context_instance=RequestContext(request)
    )
