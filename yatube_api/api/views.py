from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from posts.models import Post, Group, Comment
from .permissions import PostAuthorOnly
from .serializers import (
    PostSerializer,
    GroupSerializer,
    CommentSerializer
)


class PostViewSet(viewsets.ModelViewSet):
    """Вьюсет, отображающий информацию о всех постах и позволяющий
    создать, отредактировать или удалить пост."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [PostAuthorOnly, IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет, отображающий информацию о всех группах."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет, отображающий информацию о комментариях поста и позволяющий
    создать, отредактировать или удалить комментарий."""
    serializer_class = CommentSerializer
    permission_classes = [PostAuthorOnly, IsAuthenticated]

    def post_finding(self):
        return get_object_or_404(Post, id=self.kwargs.get('post_id'))

    def get_queryset(self):
        return Comment.objects.filter(post=CommentViewSet.post_finding(self))

    def perform_create(self, serializer):
        serializer.save(author=self.request.user,
                        post=CommentViewSet.post_finding(self))
