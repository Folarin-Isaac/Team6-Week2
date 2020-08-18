from django.db import models
#from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import datetime, timedelta

User = get_user_model()


def default_start_time():
    now = datetime.now()
    start = now.replace(hour=22, minute=0, second=0, microsecond=0)
    return start if start > now else start + timedelta(days=1)


categories_choices = (
    ('art & architecture', 'Art & Architecture'),
    ('boating & aviation', 'Boating & Aviation'),
    ('business & finance', 'Business & Finance'),
    ('cars & motorcycles', 'Cars & Motorcycles'),
    ('celebrity & gossip', 'Celebrity & Gossip'),
    ('comics & manga', 'Comics & Manga'),
    ('crafts', 'Crafts'),
    ('culture & literature', 'Culture & Literature'),
    ('family & parenting', 'Family & Parenting'),
    ('fashion', 'Fashion'),
    ('food & wine', 'Food & Wine'),
    ('health & fitness', 'Health & Fitness'),
    ('home & garden', 'Home & Garden'),
    ('hunting & fishing', 'Hunting & Fishing'),
    ('kids & teen', 'Kids & Teen'),
    ('luxury', 'Luxury'),
    ('men\'s lifestyle', 'Men\'s Lifestyle'),
    ('movies, tv & music', 'Movies, Tv & Music'),
    ('news & politics', 'News & Politics'),
    ('Photography', 'Photography'),
    ('science & engineering', 'Science & Engineering'),
    ('sports', 'Sports'),
    ('tech & gaming', 'Tech & Gaming'),
    ('travel & outdoor', 'Travel & Outdoor'),
    ('women\'s lifestyle', 'Women\'s Lifestyle'),
    ('adult +18', 'Adult +18'),
)


class ArticleModel(models.Model):
    title = models.CharField(max_length=255)
    cover_image = models.ImageField(blank=True, null=True, upload_to='images/')
    description = models.TextField(blank=True, null=True)
    author = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)
    publish = models.BooleanField(default=False)
    categories = models.CharField(max_length=50, choices=categories_choices, default='fashion')
    objects = models.Manager()

    def __str__(self):
        return self.title


class ImageModel(models.Model):
    article = models.ForeignKey(ArticleModel, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')
    image_description = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.article


class TextModel(models.Model):
    article = models.ForeignKey(ArticleModel, default=None, on_delete=models.CASCADE)
    header = models.CharField(max_length=255, null=True, blank=True)
    text = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.article
