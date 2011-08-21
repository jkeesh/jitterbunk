import facebook
from django.http import HttpResponse
from django.shortcuts import render_to_response

def index(request):
    """
    The main view for the site.
    @author Eric Conner
    """
    return render_to_response("index.html")