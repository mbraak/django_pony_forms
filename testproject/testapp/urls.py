from django.conf.urls.defaults import patterns, url

import views


urlpatterns = patterns('',
    url(r'^$', views.Index.as_view(), name='index')
)
