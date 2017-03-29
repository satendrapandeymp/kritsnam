from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import TemplateView

app_name = 'chain'

urlpatterns = [

    # Basic Things For User
    url(r'^$', login_required(views.index) , name='index'),
    url(r'^sensors/$', login_required(views.sensors) , name='sensors'),
    url(r'^sensor/$', login_required(views.sensor) , name='sensor'),
    url(r'^datas/$', login_required(views.datas) , name='datas'),
    url(r'^data/$', login_required(views.data) , name='data'),

    # test -- Will Remove after Completing Project
    url(r'^test/(?P<names>[a-z,A-Z,_,1-9]+)/$', login_required(views.csv_out) , name='test'),
    url(r'^otp/(?P<names>[a-z,A-Z,_,1-9]+)/', views.test , name='test'),
    url(r'^set_pass/(?P<names>[a-z,A-Z,_,1-9]+)/', views.set_pass , name='set_pass'),


    #for User To getting Permission for our website
    url(r'^login/$', views.login_user , name='login'),
    url(r'^logout/$', login_required(views.logout_user) , name='logout'),
    url(r'^register/$', views.Register_User.as_view() , name='register'),

    # For user
    url(r'^AddUser/$', login_required(views.AddUser) , name='AddUser'),
    url(r'^UpdateUser/(?P<pk>[0-9]+)/$', login_required(views.UpdateUser.as_view()) , name='UpdateUser'),
    url(r'^change_pass/$', login_required(views.change_pass) , name='change_pass'),
    url(r'^forget_pass/$', views.forget_pass , name='forget_pass'),
]
