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
    
    def test_update_nna_validate_autonomytutor_success(self):
        self.client.force_authenticate(user=self.staff)
        autonomy_nna = NNAUser.objects.create(
            email="ol@b",
            name="name",
            surname="surname",
            document="oooooo",
            date_of_birth="2000-03-03",
            home=self.home,
            password=make_password("test"),
            is_autonomy_tutor=True,
        )
        data = {
            "autonomy_tutor": autonomy_nna.id
        }
        response = self.client.patch(self.nna_uri + str(self.nna.id) + "/", data)
        self.assertEqual(response.status_code, 200)
    
    def test_update_nna_validate_autonomytutor_failure_reflexive(self):
        self.client.force_authenticate(user=self.staff)
        autonomy_nna = NNAUser.objects.create(
            email="l@l.com",
            name="name",
            surname="surname",
            document="llllll",
            date_of_birth="2000-03-03",
            home=self.home,
            password=make_password("test"),
            is_autonomy_tutor=True,
        )
        data = {
            "autonomy_tutor": autonomy_nna.id
        }
        response = self.client.patch(self.nna_uri + str(autonomy_nna.id) + "/", data)
        self.assertEqual(response.status_code, 400)
    
    def test_update_nna_validate_autonomytutor_failure_not_true(self):
        self.client.force_authenticate(user=self.staff)
        autonomy_nna = NNAUser.objects.create(
            email="l@l.com",
            name="name",
            surname="surname",
            document="llllll",
            date_of_birth="2000-03-03",
            home=self.home,
            password=make_password("test"),
            is_autonomy_tutor=False,
        )
        data = {
            "autonomy_tutor": autonomy_nna.id
        }
        response = self.client.patch(self.nna_uri + str(self.nna.id) + "/", data)
        self.assertEqual(response.status_code, 400)
    
    def test_update_nna_validate_therapist_success(self):
        self.client.force_authenticate(user=self.staff)
        therapist = StaffUser.objects.create(
            email="k@c",
            name="name",
            surname="surname",
            is_staff=True,
            password=make_password("test"),
        )
        therapist.homes.add(self.home)
        therapist.save()
        therapist.roles.add(self.role_therapist)
        therapist.save()
        data = {
            "therapist": therapist.id
        }
        response = self.client.patch(self.nna_uri + str(self.nna.id) + "/", data)
        self.assertEqual(response.status_code, 200)
    
    def test_update_nna_validate_therapist_failure_role(self):
        self.client.force_authenticate(user=self.staff)
        data = {
            "therapist": self.staff.id
        }
        response = self.client.patch(self.nna_uri + str(self.nna.id) + "/", data)
        self.assertEqual(response.status_code, 400)
    
    def test_update_nna_validate_therapist_failure_home(self):
        self.client.force_authenticate(user=self.staff)
        therapist = StaffUser.objects.create(
            email="k@c",
            name="name",
            surname="surname",
            is_staff=True,
            password=make_password("test"),
        )
        home1 = Home.objects.create(
            name="a",
            address="b",
        )
        therapist.homes.add(home1)
        therapist.save()
        therapist.roles.add(self.role_therapist)
        therapist.save()
        data = {
            "therapist": therapist.id
        }
        response = self.client.patch(self.nna_uri + str(self.nna.id) + "/", data)
        self.assertEqual(response.status_code, 400)
    
    def test_update_nna_validate_educators_success(self):
        self.client.force_authenticate(user=self.staff)
        educator = StaffUser.objects.create(
            email="k@c",
            name="name",
            surname="surname",
            is_staff=True,
            password=make_password("test"),
        )
        educator.homes.add(self.home)
        educator.save()
        educator.roles.add(self.role_tutor)
        educator.save()
        data = {
            "educators": [educator.id]
        }
        response = self.client.patch(self.nna_uri + str(self.nna.id) + "/", data)
        self.assertEqual(response.status_code, 200)
    
    def test_update_nna_validate_educators_failure_role(self):
        self.client.force_authenticate(user=self.staff)
        data = {
            "educators": [self.staff.id]
        }
        response = self.client.patch(self.nna_uri + str(self.nna.id) + "/", data)
        self.assertEqual(response.status_code, 400)
    
    def test_update_nna_validate_educators_failure_home(self):
        self.client.force_authenticate(user=self.staff)
        educator = StaffUser.objects.create(
            email="k@c",
            name="name",
            surname="surname",
            is_staff=True,
            password=make_password("test"),
        )
        home1 = Home.objects.create(
            name="a",
            address="b",
        )
        educator.homes.add(home1)
        educator.save()
        educator.roles.add(self.role_tutor)
        educator.save()
        data = {
            "educators": [educator.id]
        }
        response = self.client.patch(self.nna_uri + str(self.nna.id) + "/", data)
        self.assertEqual(response.status_code, 400)
    
    def test_update_nna_validate_educators_failure_count(self):
        self.client.force_authenticate(user=self.staff)
        educator = StaffUser.objects.create(
            email="k@c",
            name="name",
            surname="surname",
            is_staff=True,
            password=make_password("test"),
        )
        educator.homes.add(self.home)
        educator.save()
        educator.roles.add(self.role_tutor)
        educator.save()
        educator2 = StaffUser.objects.create(
            email="l@c",
            name="name",
            surname="surname",
            is_staff=True,
            password=make_password("test"),
        )
        educator2.homes.add(self.home)
        educator2.save()
        educator2.roles.add(self.role_tutor)
        educator2.save()
        educator3 = StaffUser.objects.create(
            email="m@c",
            name="name",
            surname="surname",
            is_staff=True,
            password=make_password("test"),
        )
        educator3.homes.add(self.home)
        educator3.save()
        educator3.roles.add(self.role_tutor)
        educator3.save()
        educator4 = StaffUser.objects.create(
            email="n@c",
            name="name",
            surname="surname",
            is_staff=True,
            password=make_password("test"),
        )
        educator4.homes.add(self.home)
        educator4.save()
        educator4.roles.add(self.role_tutor)
        educator4.save()
        educator5 = StaffUser.objects.create(
            email="z@c",
            name="name",
            surname="surname",
            is_staff=True,
            password=make_password("test"),
        )
        educator5.homes.add(self.home)
        educator5.save()
        educator5.roles.add(self.role_tutor)
        educator5.save()
        data = {
            "educators": [educator.id, educator2.id, educator3.id, educator4.id, educator5.id]
        }
        response = self.client.patch(self.nna_uri + str(self.nna.id) + "/", data)
        self.assertEqual(response.status_code, 400)
    
    def test_update_nna_validate_main_educator_failure(self):
        self.client.force_authenticate(user=self.staff)
        educator = StaffUser.objects.create(
            email="k@c",
            name="name",
            surname="surname",
            is_staff=True,
            password=make_password("test"),
        )
        educator.homes.add(self.home)
        educator.save()
        educator.roles.add(self.role_tutor)
        educator.save()
        data = {
            "educators": [educator.id],
            "main_educator": self.staff.id
        }
        response = self.client.patch(self.nna_uri + str(self.nna.id) + "/", data)
        self.assertEqual(response.status_code, 400)
    
    def test_update_nna_validate_main_educator_success(self):
        self.client.force_authenticate(user=self.staff)
        educator = StaffUser.objects.create(
            email="k@c",
            name="name",
            surname="surname",
            is_staff=True,
            password=make_password("test"),
        )
        educator.homes.add(self.home)
        educator.save()
        educator.roles.add(self.role_tutor)
        educator.save()
        data = {
            "educators": [educator.id],
            "main_educator": educator.id
        }
        response = self.client.patch(self.nna_uri + str(self.nna.id) + "/", data)
        self.assertEqual(response.status_code, 200)