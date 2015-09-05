"""mytweets URL Configuration

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
from django.conf.urls import include, url, patterns
from django.contrib import admin

from tweets.views import (Index,
                          Profile,
                          PostTweet,
                          HashTagCloud,
                          Search,
                          UserRedirect,
                          MostFollowedUsers,
                          Register)

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', Index.as_view()),
                       url(r'^user/(\w+)/$', Profile.as_view()),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^user/(\w+)/post/$', PostTweet.as_view()),
                       url(r'hashtag/(\w+)/$', HashTagCloud.as_view()),
                       url(r'^search/$', Search.as_view()),
                       url(r'^login/$', 'django.contrib.auth.views.login'),
                       url(r'^logout/$', 'django.contrib.auth.views.logout'),
                       url(r'^profile/$', UserRedirect.as_view()),
                       url(r'^mostFollowed/$', MostFollowedUsers.as_view()),
                       url(r'^user/(\w+)/?page=<page_number>', Profile.as_view()),
                       url(r'register/$', Register.as_view())
                       )
