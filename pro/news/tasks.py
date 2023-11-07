from celery import shared_task

from datetime import datetime, timedelta
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .tasks.basic import get_subscribers
from .models import Post, Category


@shared_task  # уведомление о новом посте в категории
def new_post_subscription(instance):

    for category in instance.category.all():
        email_subject = 'News Portal Ultimate! Новый пост в твоём любимом разделе!'
        user_emails = get_subscribers(category)

        html = render_to_string(
            'mail/new_post.html',
            {
                'category': category,
                'post': instance,
            }
        )

        msg = EmailMultiAlternatives(
            subject=email_subject,
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=user_emails,
        )
        msg.attach_alternative(html, "text/html")
        msg.send()


@shared_task  # еженедельная рассылка (каждый понедельник в 8:00 утра)
def send_weekly_digest():
    current_date = datetime.now()
    start_date = current_date - timedelta(days=7)

    for category in Category.objects.all():
        posts = Post.objects.filter(category=category, time_in__range=(start_date, current_date))
        if posts:
            # Получаю пользователей, подписанных на категорию
            subscribers = get_subscribers(category)

            if subscribers:
                html_content = render_to_string(
                    'mail/weekly_posts.html',
                    {
                        'posts': posts,
                    }
                )

                msg = EmailMultiAlternatives(
                    subject=f'News Portal Ultimate! Категория: "{category.name}"',
                    body='',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=subscribers,
                )

                msg.attach_alternative(html_content, 'text/html')
                msg.send()