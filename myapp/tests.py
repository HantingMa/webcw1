from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import NewsStory

class NewsAppTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.story = NewsStory.objects.create(
            headline='Test Story', category='Test', region='Test Region', details='Test Details', author=self.user)

    def test_login(self):
        response = self.client.post('/login/', {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_story_unauthenticated(self):
        response = self.client.delete(f'/delete_story/{self.story.id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_news_story_list_get(self):
        response = self.client.get('/news_stories/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

    def test_news_story_create_unauthenticated(self):
        story_data = {'headline': 'New Story', 'category': 'New', 'region': 'New Region', 'details': 'New Details'}
        response = self.client.post('/news_stories/', story_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
