from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


REGISTER_USER_URL = reverse('user:register')
LOGIN_USER_URL = reverse('user:login')
LOGOUT_USER_URL = reverse('user:logout')
PROFILE_USER_URL = reverse('user:profile')
PASSWORD_CHANGE_USER_URL = reverse('user:password_change')


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTest(TestCase):

    def setUp(self):
        """Setting up a APIClient."""
        self.client = APIClient()

    def test_register(self):
        """Registering a new user succeeds."""
        data = {
            'email': 'test@gmail.com',
            'password': 'password',
            'name': '김철수',
            'address': '서울시 서초구'
        }
        response = self.client.post(REGISTER_USER_URL, data)

        user = get_user_model().objects.get(pk=response.data['id'])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(user.email, data['email'])
        self.assertEqual(user.name, data['name'])
        self.assertEqual(user.address, data['address'])
        self.assertTrue(user.check_password(data['password']))
        self.assertNotIn('password', response.data)

    def test_register_user_duplication(self):
        """Registering a new user with an existing email fails."""
        data = {
            'email': 'test@gmail.com',
            'password': 'password'
        }
        create_user(**data)

        response = self.client.post(REGISTER_USER_URL, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login(self):
        """Trying to login with a valid user succeeds."""
        data = {
            'email': 'test@gmail.com',
            'password': 'password'
        }
        create_user(**data)

        response = self.client.post(LOGIN_USER_URL, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_email_none(self):
        """Trying to login with a non-existing email fails."""
        data = {
            'email': 'test@gmail.com',
            'password': 'password'
        }

        response = self.client.post(LOGIN_USER_URL, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_wrong_password(self):
        """Trying to login with a wrong password fails."""
        data = {
            'email': 'test@gmail.com',
            'password': 'password'
        }
        create_user(**data)
        data['password'] = 'revised password'

        response = self.client.post(LOGIN_USER_URL, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_logout(self):
        """Trying to logout with a logged-in user succeeds."""
        data = {
            'email': 'test@gmail.com',
            'password': 'password'
        }
        create_user(**data)
        self.client.login(**data)

        response = self.client.post(LOGOUT_USER_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['success'],
            '성공적으로 로그아웃 되었습니다.'
        )

    def test_logout_no_validation(self):
        """Trying to logout without a logged-in user is forbidden."""
        response = self.client.post(LOGOUT_USER_URL)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_profile(self):
        """Retrieving a user profile succeeds."""
        data = {
            'email': 'test@gmail.com',
            'password': 'password',
            'name': '김철수',
            'address': '서울시 서초구'
        }
        create_user(**data)
        self.client.login(**data)
        response = self.client.get(PROFILE_USER_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['address'], data['address'])

    def test_user_profile_no_validation(self):
        """Retrieving a user profile without login is forbidden."""
        data = {
            'email': 'test@gmail.com',
            'password': 'password'
        }
        create_user(**data)
        response = self.client.get(PROFILE_USER_URL)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_profile_update(self):
        """Test updating a user profile."""
        data = {
            'email': 'test@gmail.com',
            'password': 'password'
        }
        create_user(**data)
        self.client.login(**data)
        new_data = {
            'name': '박지민',
            'address': '서울시 구로구'
        }

        response = self.client.put(PROFILE_USER_URL, new_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], new_data['name'])
        self.assertEqual(response.data['address'], new_data['address'])

    def test_password_change(self):
        """Test changing the password of a user."""
        data = {
            'email': 'test@gmail.com',
            'password': 'password'
        }
        created_user = create_user(**data)
        self.client.login(**data)
        new_data = {
            'current_password': 'password',
            'new_password': 'revised_password'
        }

        response = self.client.put(PASSWORD_CHANGE_USER_URL, new_data)
        user = get_user_model().objects.get(pk=created_user.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(user.check_password(new_data['new_password']))

    def test_password_change_fail(self):
        """Test changing the password with the wrong current password."""
        data = {
            'email': 'test@gmail.com',
            'password': 'password'
        }
        create_user(**data)
        self.client.login(**data)
        new_data = {
            'current_password': 'wrong_password',
            'new_password': 'revised_password'
        }

        response = self.client.put(PASSWORD_CHANGE_USER_URL, new_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
