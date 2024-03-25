from django.urls import path
from .views import NewsStoryList ,NewsStoryDetail, LogoutView, LoginView
app_name="myappp"


urlpatterns = [
    path('api/login', LoginView.as_view(), name='login_api'),
    path('api/logout', LogoutView.as_view(), name='logout_api'),
    path('api/stories', NewsStoryList.as_view(), name='stories_api'),
    path('api/stories/<int:pk>', NewsStoryDetail.as_view(), name='story_detail_api'),
]