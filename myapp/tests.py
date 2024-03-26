from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.test import APITestCase
from .models import NewsStory, Author

class NewsAppTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.author = Author.objects.create_user(username='testauthor', name='Test Author', password='testpassword')
        self.story = NewsStory.objects.create(
            headline='Test Story', category='Test', region='Test Region', details='Test Details', author=self.author)
class APITests(APITestCase):

    def setUp(self):
        # 创建一个用户
        self.user = User.objects.create_user(username='testuser', email='user@test.com', password='testpassword')
        # 创建一个作者，假设 Author 模型有相应的字段
        self.author = Author.objects.create(username='authoruser', name='Test Author', user=self.user)
        # 创建一条新闻故事
        self.story = NewsStory.objects.create(headline='Test Story', category='tech', region='uk', details='Test Details', author=self.author)

    def test_login(self):
        """
        测试用户登录。
        """
        url = reverse('login')
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('Welcome, testuser!' in response.data)

    def test_logout(self):

        self.client.login(username='testuser', password='testpassword')
        url = reverse('logout') 
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("Successfully logged out." in response.data)

    def test_create_story_authenticated(self):

        self.client.force_authenticate(user=self.user)
        url = reverse('newsstory-list') 
        data = {'headline': 'New Story', 'category': 'tech', 'region': 'uk', 'details': 'Details of the new story', 'author': self.author.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(NewsStory.objects.count(), 2) 

    def test_delete_story_unauthenticated(self):

        url = reverse('newsstory-detail', kwargs={'pk': self.story.pk}) 
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)