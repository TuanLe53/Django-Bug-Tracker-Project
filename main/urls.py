from django.urls import path, include
from . import views

app_name = "ticket"

urlpatterns = [
    path("", views.home, name="home"),
    path("team/<str:team_name>/tickets", views.tickets, name="tickets"),
    path("project/<int:pk>", views.project_detail, name="project_detail"),
    path("ticket/<int:pk>", views.ticket_detail, name="ticket_detail"),
    path("team/<str:team_name>", views.team, name="team"),
    path("team/<str:team_name>/kick/<int:pk>", views.kickout, name="kick"),
    path("<int:pk>/personal", views.personal, name="personal"),
    path("api/info/<str:team_name>", views.TicketInfo, name="priority_list"),
]