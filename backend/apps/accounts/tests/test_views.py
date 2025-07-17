from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from apps.accounts.models import UserProfile, UserFavorite, UserSearchHistory
from apps.businesses.models import Business


class AccountsAPITestCase(APITestCase):
    """Base test case for accounts API tests"""
    
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        
        # Create test users
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        
        self.other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='otherpass123'
        )
        
        # Create JWT tokens for authentication
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        
        # Create test business
        self.business = Business.objects.create(
            name='Test Cafe',
            address='123 Test Street',
            postcode='SW1A 1AA',
            city='London',
            business_type='cafe',
            accessibility_level=3,
            owner=self.other_user
        )
        
        # Create user profile
        self.profile = UserProfile.objects.create(
            user=self.user,
            user_type='regular',
            phone='+441234567890',
            bio='Test user bio'
        )
    
    def authenticate(self):
        """Authenticate the test client using JWT"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')


class UserProfileAPITest(AccountsAPITestCase):
    """Test cases for user profile API endpoints"""
    
    def test_get_user_profile_authenticated(self):
        """Test getting user profile when authenticated"""
        self.authenticate()
        url = reverse('accounts:user-profile')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'Test')
        self.assertEqual(response.data['last_name'], 'User')
        self.assertEqual(response.data['profile']['user_type'], 'regular')
        self.assertEqual(response.data['profile']['phone'], '+441234567890')
    
    def test_get_user_profile_unauthenticated(self):
        """Test getting user profile when not authenticated"""
        url = reverse('accounts:user-profile')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_update_user_profile(self):
        """Test updating user profile"""
        self.authenticate()
        url = reverse('accounts:user-profile')
        
        data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'profile': {
                'user_type': 'business',
                'bio': 'Updated bio',
                'business_license_number': 'BL123456'
            }
        }
        
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'Updated')
        self.assertEqual(response.data['profile']['user_type'], 'business')
        self.assertEqual(response.data['profile']['bio'], 'Updated bio')


class UserStatsAPITest(AccountsAPITestCase):
    """Test cases for user stats API endpoint"""
    
    def test_get_user_stats(self):
        """Test getting user statistics"""
        self.authenticate()
        
        # Create some test data
        UserFavorite.objects.create(user=self.user, business=self.business)
        UserSearchHistory.objects.create(user=self.user, search_query='test search')
        
        url = reverse('accounts:user-stats')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user_type'], 'regular')
        self.assertEqual(response.data['favorites_count'], 1)
        self.assertEqual(response.data['businesses_owned'], 0)
        self.assertIn('member_since', response.data)


class UserFavoritesAPITest(AccountsAPITestCase):
    """Test cases for user favorites API endpoints"""
    
    def test_list_user_favorites(self):
        """Test listing user favorites"""
        self.authenticate()
        
        # Create a favorite
        UserFavorite.objects.create(user=self.user, business=self.business)
        
        url = reverse('accounts:user-favorites-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check if response is paginated
        if 'results' in response.data:
            # Paginated response
            self.assertEqual(len(response.data['results']), 1)
            self.assertEqual(response.data['results'][0]['business_name'], 'Test Cafe')
            self.assertEqual(response.data['results'][0]['business_accessibility_level'], 3)
        else:
            # Non-paginated response
            self.assertEqual(len(response.data), 1)
            self.assertEqual(response.data[0]['business_name'], 'Test Cafe')
            self.assertEqual(response.data[0]['business_accessibility_level'], 3)
    
    def test_create_favorite(self):
        """Test creating a favorite"""
        self.authenticate()
        
        url = reverse('accounts:user-favorites-list')
        data = {'business': self.business.id}
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(UserFavorite.objects.filter(user=self.user, business=self.business).exists())
    
    def test_delete_favorite(self):
        """Test deleting a favorite"""
        self.authenticate()
        
        # Create a favorite
        favorite = UserFavorite.objects.create(user=self.user, business=self.business)
        
        url = reverse('accounts:user-favorite-detail', kwargs={'pk': favorite.pk})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(UserFavorite.objects.filter(pk=favorite.pk).exists())
    
    def test_toggle_favorite_add(self):
        """Test toggling favorite (adding)"""
        self.authenticate()
        
        url = reverse('accounts:toggle-favorite', kwargs={'business_id': self.business.id})
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['favorited'])
        self.assertIn('Added', response.data['message'])
        self.assertTrue(UserFavorite.objects.filter(user=self.user, business=self.business).exists())
    
    def test_toggle_favorite_remove(self):
        """Test toggling favorite (removing)"""
        self.authenticate()
        
        # Create existing favorite
        UserFavorite.objects.create(user=self.user, business=self.business)
        
        url = reverse('accounts:toggle-favorite', kwargs={'business_id': self.business.id})
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['favorited'])
        self.assertIn('Removed', response.data['message'])
        self.assertFalse(UserFavorite.objects.filter(user=self.user, business=self.business).exists())


class UserSearchHistoryAPITest(AccountsAPITestCase):
    """Test cases for user search history API endpoints"""
    
    def test_list_search_history(self):
        """Test listing user search history"""
        self.authenticate()
        
        # Create search history
        UserSearchHistory.objects.create(
            user=self.user,
            search_query='accessible cafes',
            search_location='London',
            business_type_filter='cafe',
            accessibility_filter=3
        )
        
        url = reverse('accounts:user-search-history')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check if response is paginated
        if 'results' in response.data:
            # Paginated response
            self.assertEqual(len(response.data['results']), 1)
            self.assertEqual(response.data['results'][0]['search_query'], 'accessible cafes')
            self.assertEqual(response.data['results'][0]['search_location'], 'London')
        else:
            # Non-paginated response
            self.assertEqual(len(response.data), 1)
            self.assertEqual(response.data[0]['search_query'], 'accessible cafes')
            self.assertEqual(response.data[0]['search_location'], 'London')
    
    def test_create_search_history(self):
        """Test creating search history"""
        self.authenticate()
        
        url = reverse('accounts:user-search-history')
        data = {
            'search_query': 'accessible restaurants',
            'search_location': 'Manchester',
            'business_type_filter': 'restaurant',
            'accessibility_filter': 4
        }
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        search = UserSearchHistory.objects.get(user=self.user, search_query='accessible restaurants')
        self.assertEqual(search.search_location, 'Manchester')
        self.assertEqual(search.accessibility_filter, 4)


class UpdateUserTypeAPITest(AccountsAPITestCase):
    """Test cases for updating user type"""
    
    def test_update_user_type_valid(self):
        """Test updating user type with valid type"""
        self.authenticate()
        
        url = reverse('accounts:update-user-type')
        data = {'user_type': 'business'}
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('business', response.data['message'])
        
        # Verify profile was updated
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.user_type, 'business')
    
    def test_update_user_type_invalid(self):
        """Test updating user type with invalid type"""
        self.authenticate()
        
        url = reverse('accounts:update-user-type')
        data = {'user_type': 'invalid_type'}
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Invalid user type', response.data['error'])
    
    def test_update_user_type_creates_profile(self):
        """Test updating user type creates profile if it doesn't exist"""
        # Create user without profile
        new_user = User.objects.create_user(
            username='newuser',
            email='newuser@example.com',
            password='password123'
        )
        
        # Create JWT token and authenticate as new user
        refresh = RefreshToken.for_user(new_user)
        access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        url = reverse('accounts:update-user-type')
        data = {'user_type': 'assessor'}
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify profile was created
        profile = UserProfile.objects.get(user=new_user)
        self.assertEqual(profile.user_type, 'assessor')
