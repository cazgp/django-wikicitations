from django.conf.urls import patterns, url

from wikicitations import views

urlpatterns = patterns('',
    url(r'^$', views.CitationsView.as_view(), name='citations_index'),
)
