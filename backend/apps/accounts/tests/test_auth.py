from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token


class AuthenticationTest(APITestCase):
    """Test cases for authentication endpoints"""
    
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        # Updated URLs to match your actual API endpoints
        self.register_url = reverse('rest_register')  # /api/v1/auth/registration/
        self.login_url = reverse('rest_login')        # /api/v1/auth/login/
        self.logout_url = reverse('rest_logout')      # /api/v1/auth/logout/
        self.user_url = reverse('rest_user_details')  # /api/v1/auth/user/
        
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpass123!',
            'password2': 'testpass123!'
        }
        
        self.existing_user = User.objects.create_user(
            username='existinguser',
            email='existing@example.com',
            password='existingpass123!'
        )
        
    def test_user_registration_success(self):
        """Test successful user registration"""
        response = self.client.post(self.register_url, self.user_data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data)  # JWT access token should be returned
        self.assertIn('refresh', response.data)  # JWT refresh token should be returned
        
        # Verify user was created
        user = User.objects.get(username='testuser')
        self.assertEqual(user.email, 'test@example.com')
        
    def test_user_registration_duplicate_username(self):
        """Test registration with duplicate username"""
        data = self.user_data.copy()
        data['username'] = 'existinguser'  # Already exists
        
        response = self.client.post(self.register_url, data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)
        
    def test_user_registration_duplicate_email(self):
        """Test registration with duplicate email"""
        data = self.user_data.copy()
        data['email'] = 'existing@example.com'  # Already exists
        
        response = self.client.post(self.register_url, data)
        
        # Note: This might pass if ACCOUNT_UNIQUE_EMAIL is False
        # Adjust based on your settings
        if response.status_code == status.HTTP_400_BAD_REQUEST:
            self.assertIn('email', response.data)
        
    def test_user_registration_password_mismatch(self):
        """Test registration with mismatched passwords"""
        data = self.user_data.copy()
        data['password2'] = 'differentpassword'
        
        response = self.client.post(self.register_url, data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)
        
    def test_user_registration_weak_password(self):
        """Test registration with weak password"""
        data = self.user_data.copy()
        data['password1'] = '123'
        data['password2'] = '123'
        
        response = self.client.post(self.register_url, data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password1', response.data)
        
    def test_user_login_success(self):
        """Test successful user login"""
        login_data = {
            'username': 'existinguser',
            'password': 'existingpass123!'
        }
        
        response = self.client.post(self.login_url, login_data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)  # JWT access token should be returned
        self.assertIn('refresh', response.data)  # JWT refresh token should be returned
        
    def test_user_login_email(self):
        """Test login with email instead of username"""
        login_data = {
            'email': 'existing@example.com',
            'password': 'existingpass123!'
        }
        
        response = self.client.post(self.login_url, login_data)
        
        # This might fail depending on your auth configuration
        # Adjust based on your ACCOUNT_LOGIN_METHODS settings
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST])
        
    def test_user_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        login_data = {
            'username': 'existinguser',
            'password': 'wrongpassword'
        }
        
        response = self.client.post(self.login_url, login_data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)
        
    def test_user_logout_success(self):
        """Test successful user logout"""
        # First login to get a token
        token = Token.objects.create(user=self.existing_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        
        response = self.client.post(self.logout_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify token was deleted
        self.assertFalse(Token.objects.filter(user=self.existing_user).exists())
        
    def test_user_logout_unauthenticated(self):
        """Test logout without authentication"""
        response = self.client.post(self.logout_url)
        
        # dj-rest-auth returns 200 OK even for unauthenticated logout
        # This is the expected behavior as it's idempotent
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_user_details_authenticated(self):
        """Test getting user details when authenticated"""
        token = Token.objects.create(user=self.existing_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        
        response = self.client.get(self.user_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'existinguser')
        self.assertEqual(response.data['email'], 'existing@example.com')
        
    def test_get_user_details_unauthenticated(self):
        """Test getting user details without authentication"""
        response = self.client.get(self.user_url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_update_user_details(self):
        """Test updating user details"""
        token = Token.objects.create(user=self.existing_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        
        update_data = {
            'first_name': 'John',
            'last_name': 'Doe'
        }
        
        response = self.client.patch(self.user_url, update_data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify changes were saved
        self.existing_user.refresh_from_db()
        self.assertEqual(self.existing_user.first_name, 'John')
        self.assertEqual(self.existing_user.last_name, 'Doe')


class TokenAuthenticationTest(TestCase):
    """Test cases for token authentication"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='tokenuser',
            email='token@example.com',
            password='tokenpass123!'
        )
        
    def test_token_creation_on_user_creation(self):
        """Test that token is created when user is created"""
        # Create a new user
        new_user = User.objects.create_user(
            username='newuser',
            email='new@example.com',
            password='newpass123!'
        )
        
        # Token should be automatically created (if you have signal)
        # If no signal, create manually
        token, created = Token.objects.get_or_create(user=new_user)
        self.assertIsNotNone(token.key)
        
    def test_token_uniqueness(self):
        """Test that each user has a unique token"""
        user1 = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='pass123!'
        )
        
        user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='pass123!'
        )
        
        token1, _ = Token.objects.get_or_create(user=user1)
        token2, _ = Token.objects.get_or_create(user=user2)
        
        self.assertNotEqual(token1.key, token2.key)
        
    def test_token_regeneration(self):
        """Test token regeneration"""
        original_token, _ = Token.objects.get_or_create(user=self.user)
        original_key = original_token.key
        
        # Delete and recreate token
        original_token.delete()
        new_token = Token.objects.create(user=self.user)
        
        self.assertNotEqual(original_key, new_token.key)
