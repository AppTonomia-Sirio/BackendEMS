from django.urls import path
from .views import (
    UserCreate,
    LoginView,
    LocationList,
    TherapistList,
    NNAStatus,
    UserData,
)


urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("register/", UserCreate.as_view(), name="register"),
    path("locations/", LocationList.as_view(), name="location"),
    path("therapists/", TherapistList.as_view(), name="therapist"),
    path("status/", NNAStatus.as_view(), name="status"),
    path("user/<str:email>/", UserData.as_view(), name="user_data"),
]
