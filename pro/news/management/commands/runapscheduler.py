import logging
from datetime import datetime, timedelta
from django.conf import settings
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from news.models import Category, Post
from news.tasks import get_subscribers

logger = logging.getLogger(__name__)


def send_weekly_digest():
    # Получаю текущую дату
    current_date = datetime.now()

    # Вычисляю начальную и конечную даты для недельного периода
    end_date = current_date
    start_date = current_date - timedelta(days=7)

    # Получаю все категории
    categories = Category.objects.all()

    for category in categories:
        posts = Post.objects.filter(category=category, time_in__range=(start_date, end_date))
        if posts:
            # Получаю пользователей, подписанных на категорию
            subscribers = get_subscribers(category)

            if subscribers:
                subject = f'News Portal Ultimate! Категория: "{category.name}"'
                message = 'Список постов за неделю:\n\n'
                for post in posts:
                    message += f'- {post.title}\n'

                from_email = settings.DEFAULT_FROM_EMAIL
                recipient_list = subscribers

                send_mail(subject, message, from_email, recipient_list)
                logger.info(f"Sent weekly digest for category: {category.name} to {', '.join(subscribers)}")


class Command(BaseCommand):
    help = "Runs apscheduler to send weekly digests."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)

        scheduler.add_job(
            send_weekly_digest,
            trigger=CronTrigger(day_of_week='sun', hour=12, minute=0),  # Запускать по воскресеньям в 12:00
            id="send_weekly_digest",
            max_instances=1,
            replace_existing=True,
        )

        logger.info("Added weekly digest: 'send_weekly_digest'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
