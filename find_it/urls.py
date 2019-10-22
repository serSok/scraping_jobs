"""find_it URL Configuration

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
from django.urls import path, include
from django.conf import settings

from scraping.views import *
from subscribers.views import * 




urlpatterns = [
    path('admin/', admin.site.urls),
    # path('index/', index),
    # path('home/', home),
    path('list/', vacancy_list, name='list'),
    path('login/', login_subscriber, name='login'),
    path('update/', update_subscriber, name='update'),
    path('contact/', contact_admin, name='contact'),
    path('create/', SubscribersCreate.as_view(), name='create'),
    path('', index, name='index'),
]


if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        path('rosetta/', include('rosetta.urls'))
    ]
