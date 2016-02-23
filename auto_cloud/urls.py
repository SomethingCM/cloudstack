from django.conf.urls import patterns, include, url
from django.contrib import admin
from views import *

urlpatterns = patterns('auto_cloud.views',
    url(r'^cloud/add1/$', 'cloud.Addcloud', name='addcloudurl1'),
    url(r'^cloud/list1/$', 'cloud.Listcloud', name='listcloudurl1'),

    url(r'^cloud/(\w+)/add/$', 'views.Addcloud', name='addcloudurl'),
    url(r'^cloud/(\w+)/addgroup/$', 'views.Addgroup', name='addgroupurl'),
    url(r'^cloud/refresh/$', 'views.refresh', name='refreshcloudurl'),
    url(r'^cloud/temres/$', 'views.TemRes', name='temrescloudurl'),
    url(r'^cloud/list/$', 'views.Listcloud', name='listcloudurl'),
    url(r'^cloud/start/(?P<id>\d+)/$', 'views.Start', name='Starturl'),
    url(r'^cloud/stop/(?P<id>\d+)/$', 'views.Stop', name='Stopurl'),
    url(r'^cloud/restart/(?P<id>\d+)/$', 'views.Restart', name='Restarturl'),
    url(r'^cloud/delete/(?P<id>\d+)/$', 'views.Delete', name='Deleteurl'),

)
    # url(r'^cloud/edit/(?P<ID>\d+)/$', 'cloud.Editcloud', name='editcloudurl'),
    # url(r'^cloud/delete/(?P<ID>\d+)/$', 'cloud.Deletecloud', name='deletecloudrurl'),