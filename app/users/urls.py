from django.urls import path
from .views import (
    LoginView,
)

# TODO: Refactor urls structure, make it more organized
urlpatterns = [
    path('login/', LoginView.as_view()),
]
