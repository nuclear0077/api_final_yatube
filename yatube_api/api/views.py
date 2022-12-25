from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import mixins

from api.permissions import IsAuthorOrReadOnlyPermission
from api.serializers import (
    CommentSerializer,
    FollowSerializer,
    GroupSerializer,
    PostSerializer,
)
from posts.models import Follow, Group, Post


class CreateListViewsSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    pass


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthorOrReadOnlyPermission,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = LimitOffsetPagination


class FollowViewSet(CreateListViewsSet):
    serializer_class = FollowSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('^following__username',)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnlyPermission,)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        post = get_object_or_404(Post, id=self.kwargs.get('post_id'))
        return post.comments.select_related('author')

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)
