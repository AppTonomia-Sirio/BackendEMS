from django.urls import path
from .views import UserViews


urlpatterns = [
    path('<int:id>/', UserViews.as_view()),
]
