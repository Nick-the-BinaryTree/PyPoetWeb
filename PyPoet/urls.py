from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name="index"),
    url(r'^submit$', views.submit, name="submit"),
    url(r'leaving', views.leaving, name="leaving"),
    url(r'update', views.update, name="update"),
]