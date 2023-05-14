from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from . import views

app_name = 'api'

router_api_v1 = routers.DefaultRouter()
router_api_v1.register('posts', views.PostViewSet, basename='posts')
router_api_v1.register('groups', views.GroupViewSet, basename='groups')
router_api_v1.register(
    r'posts/(?P<post_id>\d+)/comments',
    views.CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/', include(router_api_v1.urls)),
    path('v1/api-token-auth/', obtain_auth_token),
]
