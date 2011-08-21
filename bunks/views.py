# 3rd party libs
import facebook

# Django utils
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

# Settings and local imports
from django.conf import settings

def _create_user_profile(request):
    """
    Create the user account and profile.
    """
    graph = facebook.GraphAPI(cookie["access_token"])
    profile = graph.get_object("me")
    
    try:
        user = User.objects.get(username=profile['username'])
    except User.DoesNotExist:
        user = User.objects.create_user(profile['username'],
                    email='test@example.com',
                    password=profile['username'])
        user.first_name = profile['first_name']
        user.last_name = profile['last_name']
        user.save()
    
    up = UserProfile(user=user, id=cookie['uid'], access_token=cookie['access_token'])
    up.save()

def login(request):
    """
    Display a login page to the user.
    """
    cookie = facebook.get_user_from_cookie(request.COOKIES,
                        settings.FACEBOOK_API_KEY, settings.FACEBOOK_SECRET_KEY)
    if cookie:
        try:
            up = UserProfile.objects.get(id=cookie['uid'])

            print up.access_token

            user = up.user
        except UserProfile.DoesNotExist:
            pass
            
    
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
            "user":request.user,
            "bunks":[1,2,3],
        },
        context_instance = RequestContext(request)
    )

