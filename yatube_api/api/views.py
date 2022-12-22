from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from api.serializers import PostSerializer
from posts.models import Post


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
