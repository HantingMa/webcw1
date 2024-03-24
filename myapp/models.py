from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

# Define the Author Model
class AuthorManager(BaseUserManager):
    def create_user(self, username, name, password=None):
        if not username:
            raise ValueError('Authors must have a username')
        if not name:
            raise ValueError('Authors must have a name')

        user = self.model(
            username=username,
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

class Author(AbstractBaseUser):
    username = models.CharField(max_length=40, unique=True)
    name = models.CharField(max_length=100)
    objects = AuthorManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name
    
#class Agency(models.Model):
#    agency_name = models.CharField(max_length=255)
#    url = models.URLField()
#    agency_code = models.CharField(max_length=10)


# Define the News Story Model
    
class NewsStory(models.Model):
    CATEGORY_CHOICES = [
        ('pol', 'Politics'),
        ('art', 'Art'),
        ('tech', 'Technology'),
        ('trivia', 'Trivia'),
    ]

    REGION_CHOICES = [
        ('uk', 'United Kingdom'),
        ('eu', 'European Union'),
        ('w', 'World'),
    ]

    headline = models.CharField(max_length=64)
    category = models.CharField(max_length=6, choices=CATEGORY_CHOICES)
    region = models.CharField(max_length=2, choices=REGION_CHOICES)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    details = models.CharField(max_length=128)

    def __str__(self):
        return self.headline
    