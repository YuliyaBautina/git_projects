import time
from celery import shared_task
# import datetime
# from django.core.mail import EmailMultiAlternatives
# from django.conf import settings
# from django.template.loader import render_to_string
# from portal.models import Post, Category


@shared_task
def hello():
    time.sleep(10)
    print("Hello, world!")
# def my_job():
#     time.sleep(10)
#     print("Hello, world!")
    # today = datetime.datetime.now()
    # last_week = today - datetime.timedelta(days=7)
    # posts = Post.objects.filter(date_time__gte=last_week)
    # categories = set(posts.values_list('category__name', flat=True))
    # subscribers = set(Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True))
    #
    # html_content = render_to_string(
    #     'week_post.html',
    #     {
    #         'link': settings.SITE_URL,
    #         'posts': posts,
    #     }
    # )
    #
    # msg = EmailMultiAlternatives(
    #     subject='Статьи за неделю в вашей избранной категории',
    #     body='',
    #     from_email=settings.DEFAULT_FROM_EMAIL,
    #     to=subscribers,
    # )
    #
    # msg.attach_alternative(html_content, 'text/html')
    # msg.send()


