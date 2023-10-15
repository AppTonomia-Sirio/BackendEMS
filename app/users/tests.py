from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from . import views
from django.contrib.auth.hashers import make_password


# Create your tests here.


class TestUser(APITestCase):
    def setUp(self):
        # Create a location
        self.location = views.Location.objects.create(
            name="Test Location",
        )
        # Create a Therapist
        self.therapist = views.Therapist.objects.create(
            name="Therapist name",
            surname="Therapist surname",
            email="therapist@gmail.com",
        )
        # Create a NNA
        hashed_password = make_password("test12345test")
        self.NNA = views.NNA.objects.create(
            name="NNA name",
            surname="NNA surname",
            location=self.location,
            mentor=self.therapist,
            email="NNA@gmail.com",
            password=hashed_password,
            date_of_birth="1990-01-01",
        )
        # Create a factory
        self.factory = APIRequestFactory()

    def test_create_NNA_api_success(self):
        # Create a NNA
        data = {
            "name": "NNA name",
            "surname": "NNA surname",
            "location": self.location.id,
            "mentor": self.therapist.id,
            "email": "NNA2@gmail.com",
            "password": "NNA12345",
            "date_of_birth": "1990-01-01",
        }

        request = self.factory.post("/register/", data)
        response = views.UserCreate.as_view()(request)

        self.assertEqual(response.status_code, 201)

    def test_create_NNA_api_failure(self):
        # Create a NNA
        data = {
            "name": "NNA name",
            "surname": "NNA surname",
            "location": "wrong location",
            "mentor": "wrong mentor",
            "email": "NNA2@gmail.com",
            "password": "NNA12345",
            "date_of_birth": "1990-01-01",
        }

        request = self.factory.post("/register/", data)
        response = views.UserCreate.as_view()(request)

        self.assertEqual(response.status_code, 400)

    def test_login_api_good_success(self):
        # Login
        data = {
            "email": "NNA@gmail.com",
            "password": "test12345test",
        }

        request = self.factory.post("/login/", data)
        response = views.LoginView.as_view()(request)

        self.assertEqual(response.status_code, 200)

    def test_login_api_bad_failure(self):
        # Login
        data = {
            "email": "NNA@gmail.com",
            "password": "wrongpassword",
        }

        request = self.factory.post("/login/", data)
        response = views.LoginView.as_view()(request)

        self.assertEqual(response.status_code, 400)

    def test_status_api_success(self):
        # Get status
        request = self.factory.get(
            "/status/", HTTP_AUTHORIZATION="Token " + self.NNA.auth_token.key
        )
        response = views.NNAStatus.as_view()(request)

        self.assertEqual(response.status_code, 200)

    def test_status_api_failure(self):
        # Get status
        request = self.factory.get("/status/")
        response = views.NNAStatus.as_view()(request)

        self.assertEqual(response.status_code, 401)

    def test_status_api_forbidden(self):
        # Get status
        request = self.factory.get(
            "/status/", HTTP_AUTHORIZATION="Token " + self.therapist.auth_token.key
        )
        response = views.NNAStatus.as_view()(request)

        self.assertEqual(response.status_code, 403)

    def test_therapist_list_api(self):
        # Get therapists list
        request = self.factory.get("/therapists/")
        response = views.TherapistList.as_view()(request)

        self.assertEqual(response.status_code, 200)

    def test_location_list_api(self):
        # Get locations list
        request = self.factory.get("/locations/")
        response = views.LocationList.as_view()(request)

        self.assertEqual(response.status_code, 200)

    def test_userdata_NNA_api_success(self):
        # Get data of NNA
        request = self.factory.get(
            "/user/",
            HTTP_AUTHORIZATION="Token " + self.therapist.auth_token.key,
        )
        response = views.UserData.as_view()(request, "NNA@gmail.com")

        self.assertEqual(response.status_code, 200)

    def test_userdata_Therapist_api_success(self):
        # Get data of therapist
        request = self.factory.get(
            "/user/",
            HTTP_AUTHORIZATION="Token " + self.therapist.auth_token.key,
        )
        response = views.UserData.as_view()(request, "therapist@gmail.com")

        self.assertEqual(response.status_code, 200)

    def test_userdata_api_failure(self):
        # Get data of non existing user
        request = self.factory.get(
            "/user/",
            HTTP_AUTHORIZATION="Token " + self.therapist.auth_token.key,
        )
        response = views.UserData.as_view()(request, "wrongaddress@gmail.com")

        self.assertEqual(response.status_code, 404)

    def test_userdata_api_forbidden(self):
        # Get data of non existing user
        request = self.factory.get("/user/")
        response = views.UserData.as_view()(request, "NNA@gmail.com")

        self.assertEqual(response.status_code, 401)
    
    def test_NNAofTherapist_api_success(self):
        # Get all NNA of a therapist
        request = self.factory.get(
            "/therapist-nna/",
            HTTP_AUTHORIZATION="Token " + self.therapist.auth_token.key,)
        response = views.NNAofTherapist.as_view()(request)

        self.assertEqual(response.status_code, 200)
    
    def test_NNAofTherapist_api_forbidden(self):
        # Get all NNA of a therapist without auth
        request = self.factory.get("/therapist-nna/")
        response = views.NNAofTherapist.as_view()(request)

        self.assertEqual(response.status_code, 401)
    
    def test_NNAofTherapist_api_NNA_forbidden(self):
        # Get all NNA of a therapist with NNA auth
        request = self.factory.get(
            "/therapist-nna/",
            HTTP_AUTHORIZATION="Token " + self.NNA.auth_token.key)
        response = views.NNAofTherapist.as_view()(request)

        self.assertEqual(response.status_code, 403)