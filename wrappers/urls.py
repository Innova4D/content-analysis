from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from wrappers import views

urlpatterns = patterns('',
    url(r'^poi$', views.PointOfInterest.as_view()),
    url(r'^user$', views.User.as_view()),
    url(r'^foursquare$', views.Foursquare.as_view()),
    url(r'^web_info$', views.WebData.as_view()),
    url(r'^facebook$', views.Facebook.as_view()),
    url(r'^twitter$', views.Twitter.as_view()),
    url(r'^linkedin$', views.Linkedin.as_view()),
    url(r'^wikipedia$', views.Wikipedia.as_view()),
    
)

urlpatterns = format_suffix_patterns(urlpatterns)