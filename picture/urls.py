"""Picturer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import sys
from django.conf.urls import url
from . import views
import Picturer.settings as settings
from django.conf.urls.static import static

app_name = 'picture'

urlpatterns = [
    url(r'^home', views.homepage, name='home'),
    url(r'login', views.login, name='login'),
    url(r'register', views.register, name='register'),
    url(r'^hello', views.hello, name='hello'),
    url(r'online', views.online, name='online'),
    url(r'publish', views.publish, name='publish'),
    url(r'search', views.search, name='search'),
    url(r'show', views.show, name='show'),
    url(r'sal', views.tax_figure, name='tax_figure'),
    url(r'details', views.details, name='details'),
    url(r'addcart', views.addcart, name='addcart'),
    url(r'cutcart', views.cutcart, name='cutcart'),
    url(r'loadcart', views.loadcart, name='loadcart'),
    url(r'getaddress', views.get_address, name='getaddress'),
    url(r'setaddress', views.set_address, name='setaddress'),
    url(r'loadgoods', views.load_goods, name='loadgoods'),
    url(r'allgoods', views.all_goods, name='allgoods'),
    url(r'specialgoods', views.special_goods, name='specialgoods'),
    url(r'json', views.get_json, name='json')
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
