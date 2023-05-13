from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

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

    def perform_update(self, serializer):
        super(PostViewSet, self).perform_update(serializer)

    def perform_destroy(self, instance):
        super(PostViewSet, self).perform_destroy(instance)


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
        return self.kwargs.get('post_id')

    def get_queryset(self):
        try:
            Comment.objects.filter(post=CommentViewSet.post_finding(self))
        except Exception:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Comment.objects.filter(post=CommentViewSet.post_finding(self))

    def perform_create(self, serializer):
        try:
            serializer.save(author=self.request.user,
                            post_id=CommentViewSet.post_finding(self))
        except Exception:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def perform_update(self, serializer):
        super(CommentViewSet, self).perform_update(serializer)

    def perform_destroy(self, instance):
        super(CommentViewSet, self).perform_destroy(instance)
