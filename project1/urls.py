from django.conf.urls import url,include
from django.contrib import admin
from czo import views
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    # For Admin
    url(r'^admin/', admin.site.urls),

    # for Root
    url(r'^$', views.kritsnam , name='kritsnam'),

    # For App
    url(r'^czo/', include('czo.urls' , namespace="czo")),

    # for overwriting login_required decorators
    url(r'^accounts/login/$', views.login_user , name='login'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root= settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
