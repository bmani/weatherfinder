from django.conf.urls import url

from conditionlookup import views

urlpatterns = [
    url(r'^$', views.index, name='index')
]
