from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import PostViewSet

app_name = 'api_v1'

v1_router = DefaultRouter()
v1_router.register('posts', PostViewSet, basename='posts')

urlpatterns = [path('v1/', include(v1_router.urls)),
               path('v1/', include('djoser.urls.jwt'))
               ]

