__author__ = 'modm'
from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^movie/(?P<id>[\w]+)/$', views.detail,name="detail"),
    url(r'^yearHist$',views.yearHist),
    url(r'^query',views.query)
]
