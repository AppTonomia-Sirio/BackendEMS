from django.urls import path
from .views import *


urlpatterns = [
    path("home/<int:id>", HomeView.as_view()),
    path("homes/", HomeListView.as_view()),
    path("role/<int:id>", RoleView.as_view()),
    path("roles/", RoleListView.as_view()),
    path("nna/", NNAListCreateView.as_view()),
    path("staff/", StaffListView.as_view()),
    path("nna/<int:id>/", NNADetailView.as_view()),
    path("staff/<int:id>/", StaffDetailView.as_view()),
    path("avatars/", AvatarListView.as_view()),
    path("avatars/<int:id>", AvatarView.as_view()),
    path("login/", CustomAuthToken.as_view()),
    path('restore/code/', PasswordResetCodeView.as_view()),
    path('restore/password/', PasswordResetView.as_view()),
]
