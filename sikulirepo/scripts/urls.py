from django.conf.urls.defaults import *

urlpatterns = patterns('scripts.views',
    # Example:
    # (r'^sikulirepo/', include('sikulirepo.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
    (r'^$', 'index'),
    (r'^(?P<script_id>\d+)/$', 'detail'),
    (r'^(?P<script_id>\d+)/update/$', 'update'),
    (r'^(?P<script_id>\d+)/showsource/$', 'showsource'),
    (r'^upload_file/$', 'upload_file'),


)
