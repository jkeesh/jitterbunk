from django.conf.urls.defaults import *
from django.conf import settings
import os

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^jitterbunk/', include('jitterbunk.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)

# Jitterbunk URL's
urlpatterns += patterns('bunks.views',
    (r'^login/?$', 'login'),
    (r'^/?$', 'index'),
    (r'^profile/(?P<id>\d+)?$', 'profile'), 
    (r'^ajax/user_search', 'user_search'),
)

# static content served only in debug
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.PROJECT_ROOT}),
    )
