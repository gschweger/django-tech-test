from django.conf.urls import include, url
from django.contrib import admin
from borrow import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^borrow/', include('borrow.urls')),
    url(r'^$', views.home_page, name='home_page'),
]
