import facebook
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.utils import simplejson
from django.conf import settings
from bunks.models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth import login as django_login, logout as django_logout
from django.contrib.auth import authenticate
from django.db.models import Q
import base64
import hmac
import hashlib
import urllib
import cgi

# Find a JSON parser
try:
    import json
    _parse_json = lambda s: json.loads(s)
except ImportError:
    try:
        import simplejson
        _parse_json = lambda s: simplejson.loads(s)
    except ImportError:
        # For Google AppEngine
        from django.utils import simplejson
        _parse_json = lambda s: simplejson.loads(s)

from bunks.models import Bunk

def about(request):
    return render_to_response(
        "about.html",
        {},
        context_instance = RequestContext(request)
    )
    
def logout_view(request):
    django_logout(request)
    response =  redirect("/")
    cookiename = "fbsr_" + settings.FACEBOOK_API_KEY
    response.delete_cookie(cookiename)
    return response

def json_response(obj):
    """
    Helper method to turn a python object into json format and return an HttpResponse object.
    """
    return HttpResponse(simplejson.dumps(obj), mimetype="application/x-javascript")


def create_bunk(request):
    bunkee = request.POST['bunkee']
    bunkee_user = User.objects.get(pk=bunkee)
    bunk = Bunk(bunker=request.user, bunkee=bunkee_user)
    bunk.save()
    return json_response({"status": "ok"})
    

def _create_user_profile(response):
    """
    Create the user account and profile.
    """
    args = dict(
        code = response['code'],
        client_id = settings.FACEBOOK_API_KEY,
        client_secret = settings.FACEBOOK_SECRET_KEY,
        redirect_uri = '',
    )
    
    file = urllib.urlopen("https://graph.facebook.com/oauth/access_token?" + urllib.urlencode(args))
    try:
        token_response = file.read()
    finally:
        file.close()
        
    access_token = cgi.parse_qs(token_response)["access_token"][-1]
        
    profile = json.load(urllib.urlopen(
        "https://graph.facebook.com/me?" +
        urllib.urlencode(dict(access_token=access_token))))
    
    try:
        user = User.objects.get(username=profile['username'])
    except User.DoesNotExist:
        user = User.objects.create_user(profile['username'],
                    email='test@example.com',
                    password=profile['username'])
        user.first_name = profile['first_name']
        user.last_name = profile['last_name']
        user.save()
    
    up = UserProfile(user=user, fbid=profile['id'])
    up.save()
    return user
    
    
def urlsafe_b64decode(str):
    """Perform Base 64 decoding for strings with missing padding."""

    l = len(str)
    pl = l % 4
    return base64.urlsafe_b64decode(str.ljust(l+pl, "="))


def parse_signed_request(signed_request, secret):
    """
    Parse signed_request given by Facebook (usually via POST),
    decrypt with app secret.

    Arguments:
    signed_request -- Facebook's signed request given through POST
    secret -- Application's app_secret required to decrpyt signed_request
    """

    if "." in signed_request:
        esig, payload = signed_request.split(".")
    else:
        return {}

    sig = urlsafe_b64decode(str(esig))
    data = _parse_json(urlsafe_b64decode(str(payload)))

    if not isinstance(data, dict):
        raise SignedRequestError("Pyload is not a json string!")
        return {}

    if data["algorithm"].upper() == "HMAC-SHA256":
        if hmac.new(secret, payload, hashlib.sha256).digest() == sig:
            return data

    else:
        raise SignedRequestError("Not HMAC-SHA256 encrypted!")

    return {}


def login_view(request):
    print "IN LOGIN VIEW"
    
    
    if 'code' in request.GET:
        print 'found code'
        token = get_access_token(request.GET['code'])

        profile = json.load(urllib.urlopen(
            "https://graph.facebook.com/me?" +
            urllib.urlencode(dict(access_token=token))))

        try:
            user = User.objects.get(username=profile['username'])
        except User.DoesNotExist:
            user = User.objects.create_user(profile['username'],
                        email='test@example.com',
                        password=profile['username'])
            user.first_name = profile['first_name']
            user.last_name = profile['last_name']
            user.save()

        up = UserProfile(user=user, fbid=profile['id'])
        up.save()
        
        user = authenticate(username=user.username, password=user.username)
        
        print 'user'
        print user
        if user is not None:
            django_login(request, user)
            
            print 'is authenticated?'
            print request.user.is_authenticated()
        
    print 'redirecting /'
    return redirect('/')
    
# Redirect URLs must match in these stages
def get_access_token(code):
    args = dict(
        code = code,
        client_id = settings.FACEBOOK_API_KEY,
        client_secret = settings.FACEBOOK_SECRET_KEY,
        redirect_uri = settings.REDIRECT_URL,
    )
    
    file = urllib.urlopen("https://graph.facebook.com/oauth/access_token?" + urllib.urlencode(args))
    try:
        token_response = file.read()
    finally:
        file.close()
        
    access_token = cgi.parse_qs(token_response)["access_token"][-1]
    return access_token

def bunk_login(request):
    """
    Display a login page to the user.
    """    
    print "IN BUNK LOGIN"
    print request
    

    
   # print request
    
    # cookiename = "fbsr_" + settings.FACEBOOK_API_KEY
    # if cookiename in request.COOKIES:    
    #     cookie = request.COOKIES["fbsr_" + settings.FACEBOOK_API_KEY]
    #     response = parse_signed_request(cookie, settings.FACEBOOK_SECRET_KEY)
    #     
    #     try:
    #         up = UserProfile.objects.get(fbid=response['user_id'])
    #         user = up.user
    #     except UserProfile.DoesNotExist:
    #         user = _create_user_profile(response)
    #         
    #     user = authenticate(username=user.username, password=user.username)
    #     if user is not None:
    #         django_login(request, user)
    #         return HttpResponseRedirect("/")
        
    args = dict(client_id=settings.FACEBOOK_API_KEY, redirect_uri=settings.REDIRECT_URL, response_type='code')
    url = 'https://www.facebook.com/dialog/oauth/?' + urllib.urlencode(args)
    
    return render_to_response(
        "login.html",
        {
            "facebook_app_id": settings.FACEBOOK_API_KEY,
            'url': url
        },
        context_instance = RequestContext(request)
    )


def index(request):
    """
    The main view for the site.
    """
    print "in index"
    
    if request.user.is_authenticated():
        print 'was authenticated'
        pass        
    else:
        print 'logging in'
        return bunk_login(request)
        
    all_bunks = Bunk.objects.all().order_by('-created_at')[:100]
            
    return render_to_response(
        "index.html", 
        {
            "user":request.user,
            "all_bunks":all_bunks,
            "facebook_app_id": settings.FACEBOOK_API_KEY
        },
        context_instance = RequestContext(request)
    )

def profile(request, id):
    """
    Display someone's profile page to the user.
    """
    profile_user = User.objects.get(pk=id)
    viewer = request.user

    user_profile = profile_user.get_profile()
    bunks_sent = user_profile.get_bunks(Bunk.SENT)
    bunks_received = user_profile.get_bunks(Bunk.RECEIVED)
    ratio = float(len(bunks_sent)) / len(bunks_received) if bunks_received else 'Inf'
    ratio = round(ratio, 2)
    return render_to_response("profile.html", {
        "user": request.user,
        "profile_user": profile_user,
        "bunks_sent": bunks_sent,
        "bunks_received": bunks_received,
        'ratio': ratio
        },
        context_instance=RequestContext(request)
    )



def user_search(request):
    name = request.GET['q']
    parts = name.split(' ')
    if len(parts) == 2:
        users =  User.objects.filter(first_name__iexact=parts[0], last_name__istartswith=parts[1])
    users = User.objects.filter(Q(first_name__istartswith=parts[0]) | Q(last_name__istartswith=parts[0]) )    

    result = []
    for user in users:
        if user == request.user: continue
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
    
    
    
