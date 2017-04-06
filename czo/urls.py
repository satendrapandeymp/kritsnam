from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import TemplateView

app_name = 'czo'

urlpatterns = [

    # Basic Things For User
    url(r'^$', login_required(views.index) , name='index'),
    url(r'^nodes/$', login_required(views.nodes) , name='nodes'),
    url(r'^data/$', login_required(views.data) , name='data'),
    url(r'^gateway/$', login_required(views.gateway) , name='gateway'),

    # test -- Will Remove after Completing Project
    url(r'^csv/$', login_required(views.csv_out) , name='test'),
    url(r'^otp/$', views.otp , name='otp'),
    url(r'^set_pass/$', views.set_pass , name='set_pass'),

    #for User To getting Permission for our website
    url(r'^login/$', views.login_user , name='login'),
    url(r'^logout/$', login_required(views.logout_user) , name='logout'),
    url(r'^register/$', views.Register_User.as_view() , name='register'),

    # For user
    url(r'^change_pass/$', login_required(views.change_pass) , name='change_pass'),
    url(r'^forget_pass/$', views.forget_pass , name='forget_pass'),
]
