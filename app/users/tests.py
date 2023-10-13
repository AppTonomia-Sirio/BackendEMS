from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from . import views
from django.contrib.auth.hashers import make_password


# Create your tests here.

class TestUser(APITestCase):

    def setUp(self):
        # Create a location
        self.location = views.Location.objects.create(
            name='Test Location',
        )
        # Create a Therapist
        self.therapist = views.Therapist.objects.create(
            name='Therapist name',
            surname='Therapist surname',
            email='therapist@gmail.com',
        )
        # Create a NNA
        hashed_password = make_password('test12345test')
        self.NNA = views.NNA.objects.create(
            name='NNA name',
            surname='NNA surname',
            location=self.location,
            mentor=self.therapist,
            email='NNA@gmail.com',
            password=hashed_password,
            date_of_birth='1990-01-01',
        )
        # Create a factory
        self.factory = APIRequestFactory()

    def test_create_NNA_api_success(self):
        # Create a NNA
        data = {
            'name': 'NNA name',
            'surname': 'NNA surname',
            'location': self.location.id,
            'mentor': self.therapist.id,
            'email': 'NNA2@gmail.com',
            'password': 'NNA12345',
            'date_of_birth': '1990-01-01',
        }

        request = self.factory.post('/register/', data)
        response = views.UserCreate.as_view()(request)

        self.assertEqual(response.status_code, 201)

    def test_create_NNA_api_failure(self):
        # Create a NNA
        data = {
            'name': 'NNA name',
            'surname': 'NNA surname',
            'location': 'wrong location',
            'mentor': 'wrong mentor',
            'email': 'NNA2@gmail.com',
            'password': 'NNA12345',
            'date_of_birth': '1990-01-01',
        }

        request = self.factory.post('/register/', data)
        response = views.UserCreate.as_view()(request)

        self.assertEqual(response.status_code, 400)

    def test_login_api_good_success(self):
        # Login
        data = {
            'email': 'NNA@gmail.com',
            'password': 'test12345test',
        }

        request = self.factory.post('/login/', data)
        response = views.LoginView.as_view()(request)

        self.assertEqual(response.status_code, 200)

    def test_login_api_bad_failure(self):
        # Login
        data = {
            'email': 'NNA@gmail.com',
            'password': 'wrongpassword',
        }

        request = self.factory.post('/login/', data)
        response = views.LoginView.as_view()(request)

        self.assertEqual(response.status_code, 400)

    def test_therapist_list_api(self):
        # Get therapists list
        request = self.factory.get('/therapists/')
        response = views.TherapistList.as_view()(request)

        self.assertEqual(response.status_code, 200)

    def test_location_list_api(self):
        # Get locations list
        request = self.factory.get('/locations/')
        response = views.LocationList.as_view()(request)

        self.assertEqual(response.status_code, 200)
