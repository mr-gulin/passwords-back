"""
URL configuration for secrets project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls.conf import include

from app.views import csrf, LoginView, SignUpView, ProtectedView

api_urls = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='login'),
    path('sign-up/', SignUpView.as_view(), name='sign-up'),
    path('test/', ProtectedView.as_view(), name='test'),
    path('csrf/', csrf),
]

urlpatterns = [
    path('api/', include(api_urls))
]
