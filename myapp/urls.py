from django.urls import path
from .views import NewsStoryList ,NewsStoryDetail, LogoutView, LoginView #, AgencyListView

app_name="myappp"


urlpatterns = [
    path('api/stories', NewsStoryList.as_view(), name='get_stories'),
    # /api/stories/key
    path('api/stories/<int:id>', NewsStoryDetail.as_view(), name='delete_story'),
    path('api/logout', LogoutView.as_view(), name='logout'),
    path('api/login', LoginView.as_view(), name='login'),
    # path('api/directory/', AgencyListView.as_view(), name='agency_list'),
]