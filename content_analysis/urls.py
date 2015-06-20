from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tutorial.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^wrappers/', include('wrappers.urls')),
    url(r'^communities/', include('communities.urls')),
    #url(r'^docs/', include('rest_framework_swagger.urls')),
 )
    
urlpatterns += patterns('',
    url(r'^authenticate/', include('rest_framework.urls',
                               namespace='rest_framework')),
)