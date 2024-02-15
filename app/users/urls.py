from django.urls import path
from rest_framework.authtoken import views
from .views import *


urlpatterns = [
    path("home/<int:id>", HomeView.as_view()),
    path("homes/", HomeListView.as_view()),
    path("role/<int:id>", RoleView.as_view()),
    path("roles/", RoleListView.as_view()),
    path("nna/", NNAListCreateView.as_view()),
    path("staff/", StaffListCreateView.as_view()),
    path('nna/<int:id>/', NNADetailView.as_view()),
    path('staff/<int:id>/', StaffDetailView.as_view()),
    path('login/', views.obtain_auth_token)
]
