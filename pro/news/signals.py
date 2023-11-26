from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.models.signals import m2m_changed, pre_save
from django.dispatch import receiver
from .models import PostCategory, Post
from .tasks import new_post_subscription


@receiver(m2m_changed, sender=PostCategory)
def notify_subscribers(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        new_post_subscription(instance)


# Функция контроля количества публикаций постов от одного пользователя
@receiver(pre_save, sender=Post)
def validate_post_count(sender, instance, **kwargs):
    # Определяю текущие дату и время
    current_date = timezone.now().date()

    # Определяю автора поста
    author = instance.author

    # Получаю количество постов автора за день
    post_count = Post.objects.filter(author=author, time_in__date=current_date).count()

    # Если количество постов автора превышает 3, всплывает ошибку валидации
    if post_count >= 3:
        raise ValidationError('Вы не можете публиковать более трёх постов в сутки!')