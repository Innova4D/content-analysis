from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from communities import views

urlpatterns = patterns('',
    url(r'^read/?$', views.Database.as_view()),
    url(r'^read/(?P<pk>\w+[-_]?\w+)/?$', views.Community.as_view()),	
    url(r'^read/(?P<pk>\w+[-_]?\w+/[a-z]+)/?$', views.Collection.as_view()),
    url(r'^read/(?P<pk>\w+[-_]?\w+/[a-z]+/\S{1,24})/?$', views.Document.as_view()),
    url(r'^read_write/(\w+[-_]?\w+/[a-z]+)/?$', views.ModifyCollection.as_view()),
    url(r'^read_write/(\w+[-_]?\w+/[a-z]+/\S{1,24})/?$', views.ModifyDocument.as_view()),    
    
)

urlpatterns = format_suffix_patterns(urlpatterns)