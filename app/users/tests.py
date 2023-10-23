from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from . import views
from django.contrib.auth.hashers import make_password
from .models import CustomUser, Home, Role
from rest_framework.authtoken.models import Token


class UserTests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = views.UserListView.as_view()
        self.uri = '/users/'
        self.role_nna = Role.objects.create(name='NNA')
        self.role_therapist = Role.objects.create(name='Therapist')
        self.role_admin = Role.objects.create(name='Admin')
        self.home = Home.objects.create(name='Home1', address='Address1')

        self.user = CustomUser.objects.create(
            name='Test',
            surname='Test',
            email='email@test.com',
            password=make_password('test'),
            document='123456789',
            date_of_birth='1990-01-01',
            home=self.home,
        )
        self.user.roles.add(self.role_nna)

        self.token = Token.objects.get(user=self.user)

    def test_login_success(self):
        data = {
            'email': 'email@test.com',
            'password': 'test'
        }

        token = Token.objects.get(user=self.user)
        request = self.factory.post(self.uri, data)
        response = views.LoginView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['token'], token.key)

    def test_login_failure(self):
        data = {}
        request = self.factory.post(self.uri, data)
        response = views.LoginView.as_view()(request)
        self.assertEqual(response.status_code, 400)

    def test_login_failure_wrong_credentials(self):
        data = {
            'email': 'worng@wrong.com',
            'password': 'wrong'
        }
        request = self.factory.post(self.uri, data)
        response = views.LoginView.as_view()(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['error'], 'Wrong Credentials')

    def test_register(self):
        data = {
            'name': 'Test2',
            'surname': 'Test2',
            'email': 'email2@test.com',
            'password': 'test2',
            'document': '123456789',
            'date_of_birth': '1990-01-01',
            'home': self.home.id,
            'roles': [self.role_nna.id],
        }
        request = self.factory.post(self.uri, data)
        response = views.UserCreate.as_view()(request)
        self.assertEqual(response.status_code, 201)

    def test_register_failure(self):
        data = {
            'name': 'Test2',
            'surname': 'Test2',
            'email': 'email2@test.com',
            'password': 'test2',
            'document': '123456789',
            'date_of_birth': '1990-01-01',
            'home': self.home.id,
            'roles': [self.role_nna.id],
        }

        request = self.factory.post(self.uri, data)
        views.UserCreate.as_view()(request)
        response = views.UserCreate.as_view()(request)
        self.assertEqual(response.status_code, 400)

    def test_get_current_user(self):
        request = self.factory.get(self.uri)
        request.META['HTTP_AUTHORIZATION'] = 'Token ' + self.token.key
        response = views.CurrentUserView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['email'], self.user.email)

    def test_get_current_user_failure(self):
        request = self.factory.get(self.uri)
        response = views.CurrentUserView.as_view()(request)
        self.assertEqual(response.status_code, 401)

    def test_get_user_list(self):
        request = self.factory.get(self.uri)
        request.META['HTTP_AUTHORIZATION'] = 'Token ' + self.token.key
        response = views.UserListView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['email'], self.user.email)

    def test_get_user_list_failure(self):
        request = self.factory.get(self.uri)
        response = views.UserListView.as_view()(request)
        self.assertEqual(response.status_code, 401)

    def test_get_user_detail(self):
        request = self.factory.get(self.uri)
        request.META['HTTP_AUTHORIZATION'] = 'Token ' + self.token.key
        response = views.UserDetailView.as_view()(request, id=self.user.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['email'], self.user.email)

    def test_get_user_detail_failure(self):
        request = self.factory.get(self.uri)
        response = views.UserDetailView.as_view()(request, id=self.user.id)
        self.assertEqual(response.status_code, 401)

    def test_partially_update_user(self):
        data = {
            'name': 'Test2'
        }
        request = self.factory.patch(self.uri, data)
        request.META['HTTP_AUTHORIZATION'] = 'Token ' + self.token.key
        response = views.UserDetailView.as_view()(request, id=self.user.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Test2')

    def test_partially_update_user_failure(self):
        data = {
            'name': 'Test2'
        }
        request = self.factory.patch(self.uri, data)
        response = views.UserDetailView.as_view()(request, id=self.user.id)
        self.assertEqual(response.status_code, 401)

    def test_delete_user_forbidden(self):
        request = self.factory.delete(self.uri)
        request.META['HTTP_AUTHORIZATION'] = 'Token ' + self.token.key
        response = views.UserDetailView.as_view()(request, id=self.user.id)
        self.assertEqual(response.status_code, 403)

    def test_homes_list(self):
        request = self.factory.get(self.uri)
        request.META['HTTP_AUTHORIZATION'] = 'Token ' + self.token.key
        response = views.HomeListView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['name'], self.home.name)

    def test_homes_list_failure(self):
        request = self.factory.get(self.uri)
        response = views.HomeListView.as_view()(request)
        self.assertEqual(response.status_code, 401)

    def test_roles_list(self):
        request = self.factory.get(self.uri)
        request.META['HTTP_AUTHORIZATION'] = 'Token ' + self.token.key
        response = views.RoleListView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['name'], self.role_nna.name)

    def test_roles_list_failure(self):
        request = self.factory.get(self.uri)
        response = views.RoleListView.as_view()(request)
        self.assertEqual(response.status_code, 401)

    def test_get_home(self):
        request = self.factory.get(self.uri)
        request.META['HTTP_AUTHORIZATION'] = 'Token ' + self.token.key
        response = views.HomeView.as_view()(request, id=self.home.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], self.home.name)

    def test_get_home_failure(self):
        request = self.factory.get(self.uri)
        response = views.HomeView.as_view()(request, id=self.home.id)
        self.assertEqual(response.status_code, 401)

    def test_get_role(self):
        request = self.factory.get(self.uri)
        request.META['HTTP_AUTHORIZATION'] = 'Token ' + self.token.key
        response = views.RoleView.as_view()(request, id=self.role_nna.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], self.role_nna.name)

    def test_get_role_failure(self):
        request = self.factory.get(self.uri)
        response = views.RoleView.as_view()(request, id=self.role_nna.id)
        self.assertEqual(response.status_code, 401)


