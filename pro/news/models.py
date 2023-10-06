from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from django.db.models.functions import Coalesce


# Определяю типы постов: "Статья" и "Новость"
article = 'AR'
news = 'NE'

POST_TYPES = [
    (article, 'Статья'),
    (news, 'Новость'),
]


# Модель Author представляет собой информацию об авторах
class Author(models.Model):
    name = models.CharField(max_length=255)  # Имя автора
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Связь один-к-одному с моделью User
    rating = models.IntegerField(default=0)  # Рейтинг автора

    # Метод для обновления рейтинга автора
    def update_rating(self):
        # Расчет суммарного рейтинга статей автора, умноженного на 3
        post_rating = Post.objects.filter(author=self).aggregate(
            post_rating_sum=Coalesce(Sum('rating') * 3, 0))

        # Расчет суммарного рейтинга всех комментариев автора
        comment_rating = Comment.objects.filter(user_id=self.user).aggregate(
            comments_rating_sum=Coalesce(Sum('rating'), 0))

        # Расчет суммарного рейтинга всех комментариев к статьям автора
        post_comment_rating = Comment.objects.filter(post__author__name=self.user).aggregate(
            comments_rating_sum=Coalesce(Sum('rating'), 0))

        # Общий рейтинг равен сумме рейтингов статей, комментариев и комментариев к статьям
        self.rating = (post_rating['post_rating_sum'] + comment_rating['comments_rating_sum'] +
                       post_comment_rating['comments_rating_sum'])
        self.save()

    # Возвращает имя автора как строковое представление объекта
    def __str__(self):
        return self.name


# Модель Category представляет собой категории постов
class Category(models.Model):
    name = models.CharField(unique=True, max_length=255)  # Уникальное имя категории

    # Метод для отображения информации о постах на сайте
    def __str__(self):
        return self.name


# Модель Post представляет собой посты (статьи и новости)
class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)  # Связь с моделью Author
    time_in = models.DateTimeField(auto_now_add=True)  # Дата и время создания поста
    type = models.CharField(choices=POST_TYPES, max_length=2)  # Тип поста (Статья или Новость)
    # Связь многие-ко-многим с моделью Category через PostCategory
    category = models.ManyToManyField('Category', through='PostCategory')
    title = models.TextField(max_length=255)  # Заголовок поста
    text = models.TextField()  # Текст поста
    rating = models.IntegerField(default=0)  # Рейтинг поста

    # Методы для увеличения и уменьшения рейтинга поста
    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    # Метод для предпросмотра текста поста (первых 124 символов)
    def preview(self):
        return self.text[:124] + '...' if len(self.text) > 124 else self.text

    # Метод для отображения заголовка поста на сайте
    def __str__(self):
        return self.title


# Модель PostCategory представляет связь между постами и категориями
class PostCategory(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)  # Связь с моделью Post
    category = models.ForeignKey('Category', on_delete=models.CASCADE)  # Связь с моделью Category


# Модель Comment представляет собой комментарии к постам
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)  # Связь с моделью Post
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Связь с моделью User
    text = models.TextField()  # Текст комментария
    time_in = models.DateTimeField(auto_now_add=True)  # Дата и время создания комментария
    rating = models.IntegerField(default=0)  # Рейтинг комментария

    # Методы для увеличения и уменьшения рейтинга комментария
    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
