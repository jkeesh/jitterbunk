import facebook
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

def index(request):
    """
    The main view for the site.
    @author Eric Conner
    """
    return HttpResponse("Hello World!")


def profile(request, id):

    return render_to_response("profile.html", {
        "viewer": request.user,
        "id": id,
        },
        context_instance=RequestContext(request)
    )
