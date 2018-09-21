"""kubernetesWebs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.contrib import admin

from k8sweb.views import index, images, services, application, colony, detail, aa, configure, jsonConfigure

urlpatterns = [
    url(r'^$', index),
    url(r'^index/$', index),
    url(r'^images/$', images),
    url(r'^service/$', services),
    url(r'^application/$', application),
    url(r'^application/detail/$', detail),
    url(r'^colony/$', colony),
    url(r'^aa/$', aa),


    url(r'^configure/$', configure),
    url(r'^jsonConfigure/$', jsonConfigure),




]
