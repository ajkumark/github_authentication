from django.conf.urls import include, url
from django.contrib import admin

from github import views

urlpatterns = [
	url(r'^$', views.home, name='home'),
	url(r'^github_oauth/$', views.github_oauth, name='github_oauth'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^create_repo/$', views.create_repo, name='create_repo'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^admin/', include(admin.site.urls)),
]
