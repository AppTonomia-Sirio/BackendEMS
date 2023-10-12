from django.urls import path
from .views import UserCreate, LoginView, LocationList, TherapistList


urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("register/", UserCreate.as_view(), name="register"),
    path("locations/", LocationList.as_view(), name="location"),
    path("therapists/", TherapistList.as_view(), name="therapist")
]
