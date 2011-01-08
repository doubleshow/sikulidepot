from django.conf.urls.defaults import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^sikulirepo/', include('sikulirepo.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
    (r'^$','scripts.views.index'),
    (r'^scripts/', include('scripts.urls')),
#    (r'^(?P<script_id>\d+)/$', 'scripts.views.showsource'),
    (r'^(?P<script_shorturl>\w+)/$','scripts.views.shorturl'),  
)


urlpatterns += staticfiles_urlpatterns()
