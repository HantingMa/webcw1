from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import NewsStory, Author

class MyAppTests(APITestCase):

    def setUp(self):
        # 设置测试客户端和测试数据
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.author = Author.objects.create(username='author1', name='Author One')
        self.news_story = NewsStory.objects.create(
            author=self.author,
            headline='Test Headline',
            category='pol',
            region='eu',
            details='Test details'
        )

    def test_logout(self):
        # 测试登出功能
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(str(response.data), '"You have been logged out."')

    def test_get_news_stories(self):
        # 测试获取新闻故事列表
        response = self.client.get(reverse('get_stories'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)

    def test_delete_news_story(self):
        # 测试删除新闻故事
        self.client.force_authenticate(user=self.user)  # 模拟用户认证
        response = self.client.delete(reverse('delete_story', kwargs={'id': self.news_story.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(NewsStory.objects.count(), 0)

