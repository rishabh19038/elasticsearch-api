from django.urls import re_path
from rest_framework import routers

from .views import get_dataset, search_dataset, get_home

router = routers.DefaultRouter()

urlpatterns = [
    re_path(r'^get-dataset/$', get_dataset),
    re_path(r'^search-dataset/$', search_dataset),
    re_path(r'^$', get_home)
]