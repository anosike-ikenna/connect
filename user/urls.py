from django.urls import re_path
from user import views

urlpatterns = [
    re_path(r"^send_login_email$", views.send_login_email, name="send_login_email"),
    re_path(r"^signup/$", views.signup, name="signup"),
    re_path(r"^login$", views.login, name="login")
]