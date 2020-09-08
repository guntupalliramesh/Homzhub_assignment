"""User_Application URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from Request_app.views import RequestView, Logout, Login, Signup, AddRequest, ReqDetail, OpenAssignment2
from rest_framework import routers
from django.views.static import serve
from Request_app import views
from django.conf.urls import include, url
from Request_app.models import UserRequest

router = routers.DefaultRouter()
router.register(r'Request', views.RequestViewSet, basename=UserRequest)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RequestView, name='request'),
    path('request/', RequestView, name='request'),
    path('Login/', Login, name='Login'),
    path('Logout/', Logout, name='Logout'),
    path('Signup/',Signup, name='Signup'),
    path('AddRequest/', AddRequest, name='AddRequest'),
    path('RawData/', include(router.urls)),
    path('OpenAssignment2/', OpenAssignment2, name='OpenAssignment2'),
    path('ReqDetail/<id>/', ReqDetail, name='ReqDetail'),
]
