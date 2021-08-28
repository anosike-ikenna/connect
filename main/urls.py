from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r"^$", views.home_page, name="home"),
    re_path(r"^(?P<id>.+)/timeline/$", views.view_timeline, name="view_timeline"),
]