from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views

app_name = 'api'


urlpatterns = [
    path('api/v1/posts/', views.PostViewSet),
    path('api/v1/api-token-auth/', obtain_auth_token),
    path('api/v1/posts/<int:post_id>/', views.PostDetailViewSet),
    path('api/v1/groups/', views.GroupViewSet),
    path('api/v1/groups/<int:group_id>/', views.GroupDetailViewSet),
    path('api/v1/posts/<int:post_id>/comments/', views.CommentViewSet),
    path('api/v1/posts/<int:post_id>/comments/<int:comment_id>/',
         views.CommentDetailViewSet),
]
