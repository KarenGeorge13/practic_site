from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    photo = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True, verbose_name='Фотокарточка')
    about = models.TextField(blank=True, verbose_name='О себе')

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['username']


class Article(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    annotation = models.TextField(blank=True, verbose_name='Аннотация', max_length=200)
    text = models.TextField(blank=True, verbose_name='Текст новости')
    user = models.ForeignKey('User', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-created_at']


class Comment(models.Model):
    topic = models.CharField(max_length=200, verbose_name='Тема')
    text = models.TextField(blank=True, verbose_name='Текст')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    article = models.ForeignKey('Article', on_delete=models.CASCADE)

    def __str__(self):
        return self.topic

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['created_at']
