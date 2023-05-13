from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from . import views

app_name = 'api'

RouterApiV1 = routers.DefaultRouter()
RouterApiV1.register('posts', views.PostViewSet, basename='posts')
RouterApiV1.register('groups', views.GroupViewSet, basename='groups')
RouterApiV1.register(
    r'posts/(?P<post_id>\d+)/comments',
    views.CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/', include(RouterApiV1.urls)),
    path('v1/api-token-auth/', obtain_auth_token),
]
