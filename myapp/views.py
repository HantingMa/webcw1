# Django 相关导入
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.dateparse import parse_date
from django.contrib.auth import logout,authenticate, login
from django.utils import timezone

# REST framework 相关导入
from rest_framework import status, views, viewsets, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

# 本地应用的导入
from .models import NewsStory, Post#, Agency
from .serializers import NewsStorySerializer, PostSerializer #, AgencySerializer


def index(request):
    context = {'message': 'Hello, this is myapp!'}
    return render(request, 'myapp/index.html', context)

# create api views


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer



class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response("You have been logged out.", status=status.HTTP_200_OK, content_type='text/plain')
# new story
class NewsStoryList(APIView):
    def handle(self, request, format=None):
        if request.method == "GET":
            category = request.query_params.get('story_cat', '*')
            region = request.query_params.get('story_region', '*')
            date_str = request.query_params.get('story_date', '*')
            
            stories = NewsStory.objects.all()
            
            if category != '*':
                stories = stories.filter(category=category)
            if region != '*':
                stories = stories.filter(region=region)
            if date_str != '*':
                date = parse_date(date_str)
                stories = stories.filter(date__gte=date) if date else stories
            
            if stories:
                serializer = NewsStorySerializer(stories, many=True)
                return Response(serializer.data)
            else:
                return Response('No stories found', status=status.HTTP_404_NOT_FOUND)

        # Handling POST requests
        elif request.method == "POST":
            if not request.user.is_authenticated:
                return Response("Unauthorized", status=status.HTTP_401_UNAUTHORIZED)

            data = request.data
            data['author'] = request.user.author.id  # Assuming Author is related to User
            data['date'] = timezone.now()

            serializer = NewsStorySerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Directing both GET and POST requests to the same handler method
    def get(self, request, *args, **kwargs):
        return self.handle(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.handle(request, *args, **kwargs)
# delet view


class NewsStoryDetail(generics.DestroyAPIView):
    queryset = NewsStory.objects.all()
    lookup_field = 'id'  # Assuming 'id' is the field you use to identify the story

    def delete(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response('Authentication required', status=status.HTTP_401_UNAUTHORIZED)
        return super(NewsStoryDetail, self).delete(request, *args, **kwargs)
    
class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        logout(request)
        return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
    
class DeleteStoryView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, key, format=None):
        try:
            story = NewsStory.objects.get(pk=key)
            if request.user != story.author.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            story.delete()
            return Response(status=status.HTTP_200_OK)
        except NewsStory.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(str(e), status=status.HTTP_503_SERVICE_UNAVAILABLE)
    
class LoginView(APIView):
    def post(self, request, format=None):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return Response(f"Welcome, {username}!", status=status.HTTP_200_OK)
        else:
            return Response("Login failed. Check username and password.", status=status.HTTP_401_UNAUTHORIZED)
