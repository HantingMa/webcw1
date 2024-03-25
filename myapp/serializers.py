# myapp/serializers.py

from rest_framework import serializers
from .models import NewsStory
from .models import Post
#from .models import Agency

class NewsStorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsStory
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'