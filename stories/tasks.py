from celery import shared_task
from datetime import datetime, timedelta

from stories.models import Story, StoryStream

@shared_task
def check_stories_date():
    expiration_date = datetime.now() - timedelta(hours=24)
    old_stories = Story.objects.filter(posted__lt=expiration_date)
    old_stories.update(expired=True)
    print('Stories expiration updated!')

@shared_task
def delete_expired():
    Story.objects.filter(expired=True).delete()
    StoryStream.objects.filter(story=None).delete()
    print('Story Stream delete of deleted story.')
