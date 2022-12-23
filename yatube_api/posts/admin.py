from django.contrib import admin

from .models import Comment, Follow, Group, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'text',
        'pub_date',
        'author',
        'group',
    )
    list_editable = ('group',)
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


@admin.register(Comment)
class CommentsAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'author',
        'text',
        'post',
        'created',
    )
    list_filter = ('created',)
    search_fields = ('text',)
    empty_value_display = '-пусто-'


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user',
        'following',
    )
    list_filter = (
        'user',
        'following',
    )
    search_fields = (
        'user',
        'following',
    )
    empty_value_display = '-пусто-'


admin.site.register(
    Group,
)