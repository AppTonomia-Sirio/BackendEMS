from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from .views import *
from django.contrib.auth.hashers import make_password
from .models import *
from rest_framework.authtoken.models import Token


class UserTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.uri = "/users/"
        self.nna_uri = self.uri + "nna/"
        self.staff_uri = self.uri + "staff/"
        self.home_uri = self.uri + "home/"
        self.role_uri = self.uri + "role/"
        self.role_tutor = Role.objects.get(name="Educador Tutor")
        self.role_therapist = Role.objects.get(name="Terapeuta")
        self.role_social_worker = Role.objects.get(name="Trabajador Social")
        self.home = Home.objects.create(name="Home1", address="Address1")
        self.home2 = Home.objects.create(name="Home2", address="Address2")

        self.user = CustomUser.objects.create(
            name="Test",
            surname="Test",
            email="email@test.com",
            password=make_password("test"),
            is_staff=False,
        )
        self.nna = NNAUser.objects.create(
            email="b@b",
            name="name",
            surname="surname",
            document="document",
            date_of_birth="2000-03-03",
            home=self.home,
            password=make_password("test"),
        )
        self.staff = StaffUser.objects.create(
            email="c@c",
            name="name",
            surname="surname",
            is_staff=True,
            password=make_password("test"),
        )
        self.staff.homes.add(self.home)
        self.staff.save()
        self.staff.roles.add(self.role_social_worker)
        self.staff.save()

        self.avatar = Avatar.objects.create()

        self.token = Token.objects.get(user=self.user)

    def test_token_created(self):
        token = Token.objects.get(user=self.user)
        self.assertEqual(token.key, self.token.key)

    def test_nna_list_unauthenticated(self):
        response = self.client.get(self.nna_uri)
        self.assertEqual(response.status_code, 401)

    def test_nna_list_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.get(self.nna_uri)
        self.assertEqual(response.status_code, 200)

    def test_create_nna_staff(self):
        self.client.force_authenticate(user=self.staff)
        data = {
            "email": "d@d.com",
            "name": "name",
            "surname": "surname",
            "document": "documentt",
            "date_of_birth": "2000-03-03",
            "home": self.home.id,
            "password": "test",
        }
        response = self.client.post(self.nna_uri, data)
        self.assertEqual(response.status_code, 201)

    def test_create_nna_not_staff(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "email": "d@d.com",
            "name": "name",
            "surname": "surname",
            "document": "document",
            "date_of_birth": "2000-03-03",
            "home": self.home.id,
            "password": "test",
        }
        response = self.client.post(self.nna_uri, data)
        self.assertEqual(response.status_code, 403)

    def create_nna_forbidden_fields_staff(self):
        self.client.force_authenticate(user=self.staff)
        data = {
            "email": "d@d.com",
            "name": "name",
            "surname": "surname",
            "document": "document",
            "date_of_birth": "2000-03-03",
            "home": self.home.id,
            "password": "test",
            "autonomy_level": 5,
        }
        response = self.client.post(self.nna_uri, data)
        self.assertEqual(response.status_code, 201)

    def create_nna_forbidden_fields_not_staff(self):
        data = {
            "email": "d@d.com",
            "name": "name",
            "surname": "surname",
            "document": "document",
            "date_of_birth": "2000-03-03",
            "home": self.home.id,
            "password": "test",
            "autonomy_level": 5,
        }
        response = self.client.post(self.nna_uri, data)
        self.assertEqual(response.status_code, 403)

    def test_staff_list_unauthenticated(self):
        response = self.client.get(self.staff_uri)
        self.assertEqual(response.status_code, 401)

    def test_staff_list_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.get(self.staff_uri)
        self.assertEqual(response.status_code, 200)

    def test_nna_detail_unauthenticated(self):
        response = self.client.get(self.nna_uri + str(self.nna.id) + "/")
        self.assertEqual(response.status_code, 401)

    def test_nna_detail_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.get(self.nna_uri + str(self.nna.id) + "/")
        self.assertEqual(response.status_code, 200)

    def test_update_nna_superuser(self):
        self.client.force_authenticate(user=self.staff)
        data = {
            "email": "d@d.com",
            "name": "name",
            "surname": "surname",
            "document": "document",
            "date_of_birth": "2000-03-03",
            "home": self.home.id,
            "password": "test",
        }
        response = self.client.put(self.nna_uri + str(self.nna.id) + "/", data)
        self.assertEqual(response.status_code, 200)

    def test_update_nna_not_superuser(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "email": "d@d.com",
            "name": "name",
            "surname": "surname",
            "document": "document",
            "date_of_birth": "2000-03-03",
            "home": self.home.id,
            "password": "test",
        }
        response = self.client.put(self.nna_uri + str(self.nna.id) + "/", data)
        self.assertEqual(response.status_code, 403)

    def test_staff_detail_unauthenticated(self):
        response = self.client.get(self.staff_uri + str(self.staff.id) + "/")
        self.assertEqual(response.status_code, 401)

    def test_staff_detail_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.get(self.staff_uri + str(self.staff.id) + "/")
        self.assertEqual(response.status_code, 200)

    def test_update_staff_not_superuser(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "email": "d@d.com",
            "name": "name",
            "surname": "surname",
            "is_staff": True,
            "password": "test",
        }
        response = self.client.put(self.staff_uri + str(self.staff.id) + "/", data)
        self.assertEqual(response.status_code, 403)
