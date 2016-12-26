from django.conf.urls import patterns, include, url
from django.views.decorators.csrf import csrf_exempt
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ADTO_TOOLS.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^home/', 'Galactic_Warships.views.top'),
    url(r'getsidebar/', 'Galactic_Warships.views.sidebar_content'),
    #url(r'getsidebar/', csrf_exempt('Galactic_Warships.views.sidebar_content'), name='sidebar_content'),
    url(r'getrr/', 'Galactic_Warships.views.rr_list'),
    url(r'build/', 'Galactic_Warships.views.build_project'),
    url(r'deploy/', 'Galactic_Warships.views.deploy_project'),
    url(r'op_online/', 'Galactic_Warships.views.operation_online'),
    url(r'lock_online/', 'Galactic_Warships.views.lock_online'),
    url(r'getserverlist/', 'Galactic_Warships.views.show_privilege_list'),
    url(r'record_privilege/', 'Galactic_Warships.views.record_privilege'),
)
