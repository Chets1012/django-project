"""home1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
# from django.urls import path
# from home12 import views
# from django.contrib.auth import views as auth_views
from django.conf.urls import url, include
from django.conf import settings
from home12.views import (login_view, register_view, logout_view, index, contact, profile, pro, UserUpdate, UserDelete)
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
urlpatterns = [
    # url(r'^admin/$', admin.site.urls),
    # url(r'^$',views.index,name='index'),
    # url(r'^contact/$',views.contact,name='contact'),
    # url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    # url(r'^login/$',auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    # url(r'^logout/$', auth_views.LogoutView,{'next_page': settings.LOGIN_REDIRECT_URL}, name='logout'),
    # url(r'^signup/$', views.signup, name='signup'),
     url(r'^admin/', admin.site.urls),
    # Accounts
    # url(r'^register/$', face_r, name='faceR'),
    url(r'^login/$', login_view, name='login'),
    url(r'^register/$', register_view, name='register'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^$',index,name='index'),
    url(r'^contact/$',contact,name='contact'),
    # url(r'^profile/$',profile,name='profile'),
    url(r'^profile/$',pro,name='profile'),
    path('edit/<int:pk>', UserUpdate.as_view(), name='user_edit'),
    path('delete/<int:pk>', UserDelete.as_view(), name='user_delete'),
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

