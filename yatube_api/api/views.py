from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from posts.models import Post, Group, Comment
from .serializers import (
    PostSerializer,
    GroupSerializer,
    CommentSerializer
)


class PostViewSet(viewsets.ModelViewSet):
    """Вьюсет, отображающий информацию о всех постах и позволяющий
    создать новый пост."""
    querryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetailViewSet(viewsets.ModelViewSet):
    """Вьюсет, отображающий информацию о конкретном посте и позволяющий
    его автору отредактировать или удалить его."""
    querryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_queryset(self, post_id):
        return super().get_queryset().filter(id=post_id)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        super(PostViewSet, self).perform_update(serializer)

    def perform_destroy(self, serializer):
        if serializer.instance.author != self.request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        super(PostViewSet, self).perform_destroy(serializer)


class GroupViewSet(viewsets.ModelViewSet):
    """Вьюсет, отображающий информацию о всех группах."""
    querryset = Group.objects.all()
    serializer_class = GroupSerializer


class GroupDetailViewSet(viewsets.ModelViewSet):
    """Вьюсет, отображающий информацию о конкретной группе."""
    querryset = Group.objects.all()
    serializer_class = GroupSerializer

    def get_queryset(self, group_id):
        return super().get_queryset().filter(id=group_id)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет, отображающий информацию о комментариях поста."""
    querryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self, post_id):
        return super().get_queryset().filter(post=post_id)

    def perform_create(self, serializer):
        super(CommentViewSet, self).perform_create(serializer)


class CommentDetailViewSet(viewsets.ModelViewSet):
    """Вьюсет, отображающий информацию о конкретном комментарии поста,
    и позволяющий автору отредактировать или удалить его."""
    querryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self, post_id, comment_id):
        return super().get_queryset().filter(post=post_id, id=comment_id)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        super(CommentDetailViewSet, self).perform_update(serializer)

    def perform_destroy(self, serializer):
        if serializer.instance.author != self.request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        super(CommentDetailViewSet, self).perform_destroy(serializer)
