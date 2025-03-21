from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import CustomUser

class UserRegistrationTests(APITestCase):
    def test_user_registration(self):
        """
        Ensure we can create a new user account.
        """
        url = reverse('register')
        data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'password': 'TestPassword123!',
            'password2': 'TestPassword123!'
        }
        response = self.client.post(url, data, format='json')
        
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check that user was created
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(CustomUser.objects.get().email, 'test@example.com')
        self.assertEqual(CustomUser.objects.get().name, 'Test User')

    def test_user_registration_password_mismatch(self):
        """
        Ensure user cannot register with mismatched passwords.
        """
        url = reverse('register')
        data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'password': 'TestPassword123!',
            'password2': 'DifferentPassword123!'
        }
        response = self.client.post(url, data, format='json')
        
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Check that no user was created
        self.assertEqual(CustomUser.objects.count(), 0)

    def test_user_registration_email_unique(self):
        """
        Ensure user cannot register with an email that is already in use.
        """
        # Create a user first
        CustomUser.objects.create_user(
            email='existing@example.com',
            name='Existing User',
            password='ExistingPassword123!'
        )
        
        url = reverse('register')
        data = {
            'name': 'New User',
            'email': 'existing@example.com',  # Same email
            'password': 'NewPassword123!',
            'password2': 'NewPassword123!'
        }
        response = self.client.post(url, data, format='json')
        
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Check that no new user was created
        self.assertEqual(CustomUser.objects.count(), 1)

class UserLoginTests(APITestCase):
    def setUp(self):
        """
        Create a user for login tests.
        """
        self.user = CustomUser.objects.create_user(
            email='test@example.com',
            name='Test User',
            password='TestPassword123!'
        )

    def test_user_login_success(self):
        """
        Ensure user can login and receive tokens.
        """
        url = reverse('token_obtain_pair')
        data = {
            'email': 'test@example.com',
            'password': 'TestPassword123!'
        }
        response = self.client.post(url, data, format='json')
        
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check that tokens are in response
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_user_login_invalid_credentials(self):
        """
        Ensure user cannot login with invalid credentials.
        """
        url = reverse('token_obtain_pair')
        data = {
            'email': 'test@example.com',
            'password': 'WrongPassword123!'
        }
        response = self.client.post(url, data, format='json')
        
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class UserProfileTests(APITestCase):
    def setUp(self):
        """
        Create a user and authenticate for profile tests.
        """
        # Create user
        self.user = CustomUser.objects.create_user(
            email='test@example.com',
            name='Test User',
            password='TestPassword123!'
        )
        
        # Get tokens
        url = reverse('token_obtain_pair')
        data = {
            'email': 'test@example.com',
            'password': 'TestPassword123!'
        }
        response = self.client.post(url, data, format='json')
        self.token = response.data['access']
        
        # Set authentication header
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_get_profile(self):
        """
        Ensure authenticated user can retrieve their profile.
        """
        url = reverse('profile')
        response = self.client.get(url)
        
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check profile data
        self.assertEqual(response.data['email'], 'test@example.com')
        self.assertEqual(response.data['name'], 'Test User')

    def test_update_profile(self):
        """
        Ensure authenticated user can update their profile.
        """
        url = reverse('profile')
        data = {
            'name': 'Updated User'
        }
        response = self.client.patch(url, data, format='json')
        
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check that name was updated
        self.assertEqual(response.data['name'], 'Updated User')
        
        # Verify in database
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, 'Updated User')

    def test_profile_unauthenticated(self):
        """
        Ensure unauthenticated user cannot access profile.
        """
        # Remove authentication credentials
        self.client.credentials()
        
        url = reverse('profile')
        response = self.client.get(url)
        
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class TokenRefreshTests(APITestCase):
    def setUp(self):
        """
        Create a user and get refresh token.
        """
        # Create user
        self.user = CustomUser.objects.create_user(
            email='test@example.com',
            name='Test User',
            password='TestPassword123!'
        )
        
        # Get tokens
        url = reverse('token_obtain_pair')
        data = {
            'email': 'test@example.com',
            'password': 'TestPassword123!'
        }
        response = self.client.post(url, data, format='json')
        self.refresh_token = response.data['refresh']

    def test_token_refresh(self):
        """
        Ensure refresh token can be used to get new access token.
        """
        url = reverse('token_refresh')
        data = {
            'refresh': self.refresh_token
        }
        response = self.client.post(url, data, format='json')
        
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check that new access token is in response
        self.assertIn('access', response.data)

    def test_token_refresh_invalid_token(self):
        """
        Ensure invalid refresh token cannot be used to get new access token.
        """
        url = reverse('token_refresh')
        data = {
            'refresh': 'invalid-token'
        }
        response = self.client.post(url, data, format='json')
        
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)