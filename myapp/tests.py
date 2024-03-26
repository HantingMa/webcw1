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
        url = reverse('login')  # 假设您的登录视图的 URL 名称为 'login'
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('Welcome, testuser!' in response.data)

    def test_logout(self):
        """
        测试用户登出。
        """
        # 首先登录
        self.client.login(username='testuser', password='testpassword')
        url = reverse('logout')  # 假设您的登出视图的 URL 名称为 'logout'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("Successfully logged out." in response.data)

    def test_create_story_authenticated(self):
        """
        测试认证用户创建新闻故事。
        """
        self.client.force_authenticate(user=self.user)  # 认证用户
        url = reverse('newsstory-list')  # 假设您的新闻故事列表视图的 URL 名称为 'newsstory-list'
        data = {'headline': 'New Story', 'category': 'tech', 'region': 'uk', 'details': 'Details of the new story', 'author': self.author.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(NewsStory.objects.count(), 2)  # 假设之前已经有一条故事

    def test_delete_story_unauthenticated(self):
        """
        测试未认证用户尝试删除新闻故事。
        """
        url = reverse('newsstory-detail', kwargs={'pk': self.story.pk})  # 假设您的新闻故事详情视图的 URL 名称为 'newsstory-detail'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)