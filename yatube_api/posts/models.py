from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок группы')
    slug = models.SlugField(
        unique=True, verbose_name='Имя группы в формате slug'
    )
    description = models.TextField(verbose_name='Описание группы')

    def __str__(self) -> str:
        return f'Группа: {self.title}'

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Группа',
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts'
    )
    image = models.ImageField(upload_to='posts/', null=True, blank=True)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Коментарии'


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )

    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Авторы на которых подписываются',
    )

    def __str__(self):
        return (
            f'Пользователь: {self.user.get_username()},'
            f'подписан на автора {self.following.username}'
        )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'], name='unique_user_following'
            )
        ]
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'
