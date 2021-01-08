"""hit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^home/', 'index.views.home'),
    url(r'^signup/$', 'index.views.signup'),
    url(r'^signout/$', 'index.views.signout'),
    url(r'^signup/submit/', 'index.views.signup_submit'),
    url(r'^login/$', 'index.views.login'),
    url(r'^login/submit/', 'index.views.login_submit'),
    url(r'^task/list', 'index.views.task_list'),
    url(r'^task/delete', 'index.views.task_delete'),
    url(r'^task/new', 'index.views.task_new'),
    url(r'^task/get_list', 'index.views.get_task_list'),
    url(r'^task/info/', 'index.views.task_info'),
    url(r'^task/update/', 'index.views.task_update'),
    url(r'^task/submit/', 'index.views.task_submit'),
    url(r'^task/run/', 'index.views.task_run'),
    url(r'^task/execute/', 'index.views.task_execute'),
    url(r'^check_username/', 'index.views.check_username'),
    url(r'^case/new/', 'index.views.case_new'),
    url(r'^case/submit/', 'index.views.case_submit'),
]
