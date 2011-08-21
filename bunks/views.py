import facebook
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.utils import simplejson
from django.conf import settings
from bunks.models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth import login as django_login
from django.contrib.auth import authenticate

from bunks.models import Bunk

def _create_user_profile(cookie):
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
    
    up = UserProfile(user=user, fbid=cookie['uid'])
    up.save()
    return user

def login(request):
    """
    Display a login page to the user.
    """
    cookie = facebook.get_user_from_cookie(request.COOKIES,
                        settings.FACEBOOK_API_KEY, settings.FACEBOOK_SECRET_KEY)
    if cookie and not request.user.is_authenticated():
        try:
            up = UserProfile.objects.get(fbid=cookie['uid'])
            user = up.user
        except UserProfile.DoesNotExist:
            user = _create_user_profile(cookie)
            
        user = authenticate(username=user.username, password=user.username)
        if user is not None:
            django_login(request, user)
            return HttpResponseRedirect("/")
        else:
            print "user was none"
            
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
    if request.user.is_authenticated():
        print request.user
        print request.user.get_profile().fbid
        
    all_bunks = Bunk.objects.all().order_by('-created_at')
    all_bunks = (
        {
            "bunker":"bunker",
            "bunkee":"bunkee",
            
        },
        {
            "bunker":"bunker",
            "bunkee":"bunkee",
            
        },
    )
    
    return render_to_response(
        "index.html", 
        {
            "user":request.user,
            "all_bunks":all_bunks,
        },
        context_instance = RequestContext(request)
    )

def profile(request, id):
    """
    Display someone's profile page to the user.
    """
    user = User.objects.get(pk=id)
    viewer = request.user

    user_profile = user.get_profile();
    bunks_sent = user_profile.get_bunks(Bunk.SENT);
    bunks_received = user_profile.get_bunks(Bunk.RECEIVED);

    return render_to_response("profile.html", {
        "viewer": request.user,
        "user": user,
        "bunks_sent": bunks_sent,
        "bunks_received": bunks_received,
        "bunks_sent_count": len(bunks_sent),
        "bunks_received_count": len(bunks_received),
        },
        context_instance=RequestContext(request)
    )



def user_search(request):
    name = request.GET['q']
    
    users = User.objects.all()
    
    result = []
    for user in users:
        try:
            profile = user.get_profile()
            result.append(
                {
                    "name": "%s %s" % (user.first_name, user.last_name),
                    "url": "/profile/%d" % user.id,
                    "image": "https://graph.facebook.com/%s/picture?type=square" % profile.fbid,
                    "pk":user.id,
                 }
            )
        except UserProfile.DoesNotExist:
            print "User %s either a superuser or doesn't exist" % user.id
    
    
    json = simplejson.dumps(result)
    return HttpResponse(json, mimetype="application/x-javascript")
    
    
    
