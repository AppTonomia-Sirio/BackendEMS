from django.urls import path
from .views import *


urlpatterns = [
    path("home/<int:id>", HomeView.as_view()),
    path("homes/", HomeListView.as_view()),
    path("role/<int:id>", RoleView.as_view()),
    path("roles/", RoleListView.as_view()),
]
