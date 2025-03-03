from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import timedelta
import uuid



class Content(models.Model):
    TYPE_CHOICES = [
        (0, 'Movie'),
        (1, 'Series'),
        (3, 'TV Show')
    ]

    STATUS_CHOICES = [
        (0, 'Upcoming'),
        (1, 'Released'),
        (2, 'Archived'),
    ]
    
    CATEGORY_CHOICES = [
        (0, 'Action'),
        (1, 'Adventure'),
        (2, 'Animation'),
        (3, 'Comedy'),
        (4, 'Crime'),
        (5, 'Drama'),
        (6, 'Fantasy'),
        (7, 'Historical'),
        (8, 'Horror'),
        (9, 'Mystery'),
        (10, 'Political'),
        (11, 'Romance'),
        (12, 'Sci-Fi'),
        (13, 'Thriller'),
    ]
    id = models.BigAutoField(primary_key=True, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    image_url = models.URLField(max_length=500 ,blank=True)
    trailer_url = models.URLField(max_length=500, blank=True)
    types = models.IntegerField(choices=TYPE_CHOICES) 
    category = models.IntegerField(choices=CATEGORY_CHOICES) 
    status = models.IntegerField(choices=STATUS_CHOICES, blank=True)  
    release_at = models.DateTimeField()
    start_to_end_time = models.DurationField(_('Duration of movie'), blank=True, default=timedelta(hours=4))
    reting = models.DecimalField(max_digits=3, decimal_places=1)
    ott_release_at = models.DateTimeField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        indexes = [
            models.Index(fields=['types', 'category', 'status']),
        ]

class Episode(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    content = models.ForeignKey(Content, related_name='episodes', on_delete=models.CASCADE)
    season = models.IntegerField(blank=True)
    episode_number = models.IntegerField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    release_at = models.DateTimeField()
    ott_release_at = models.DateTimeField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Season {self.season} - Episode {self.episode_number}: {self.title}"

    def save(self, *args, **kwargs):
        if self.content.types == 0:  # Movie cannot have episodes
            raise ValueError("Movies cannot have episodes.")
        super().save(*args, **kwargs)

    class Meta:
        indexes = [
            models.Index(fields=['content', 'season', 'episode_number']),
        ]


class Language(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name



class ContentLanguage(models.Model):
    content = models.ForeignKey('Content', on_delete=models.CASCADE, related_name='languages')
    language = models.ForeignKey('Language', on_delete=models.CASCADE, related_name='contents')

    def __str__(self):
        return f"{self.content.title} - {self.language.name}"

class UserSession(models.Model):
    session_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)  # Stored in cookies
    device_info = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField()
    last_seen = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.session_id)

class SearchHistory(models.Model):
    session = models.ForeignKey(UserSession, on_delete=models.CASCADE, related_name='searches')
    search_term = models.CharField(max_length=255)
    search_count = models.IntegerField(default=1)  # Tracks search count
    searched_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.session.session_id} - {self.search_term} ({self.search_count} times)"

class VisitCount(models.Model):
    session = models.ForeignKey(UserSession, on_delete=models.CASCADE, related_name='visits')
    content = models.ForeignKey('Content', on_delete=models.CASCADE, related_name='visit_counts')
    visit_count = models.IntegerField(default=0)
    last_visited = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.session.session_id} - {self.content.title} ({self.visit_count} visits)"

class Recommendation(models.Model):
    RECOMMENDATION_TYPES = [
        ('Trending', 'Trending'),
        ('Top Rated', 'Top Rated'),
        ('New Release', 'New Release'),
        ('Personalized', 'Personalized'),
    ]

    session = models.ForeignKey(UserSession, on_delete=models.CASCADE, related_name='recommendations')
    content = models.ForeignKey('Content', on_delete=models.CASCADE, related_name='recommendations')
    recommendation_type = models.CharField(max_length=50, choices=RECOMMENDATION_TYPES)
    trending_score = models.FloatField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.session.session_id} - {self.content.title} ({self.recommendation_type})"
