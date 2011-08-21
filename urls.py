from django.conf.urls.defaults import *
from django.conf import settings

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
urlpatterns += patterns('jitterbunk.bunks.views',
    (r'^/?$', 'index'),
)

# static content served only in debug
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': os.path.dirname(settings.PROJECT_ROOT)}),
    )
