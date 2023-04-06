from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("login", views.login, name="login"),
    path("register", views.register, name="register"),
    path("logout", views.logout, name="logout"),
    path("create/team", views.create_team, name="create_team"),
    path("team/join/<str:team_name>", views.join, name="join"),
]