import uuid

from .all_content import Content, Genre
from .user_models import User
from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import timedelta



class SearchHistory(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    content_id = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='search_history')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_searched = models.DateTimeField(auto_now=True)
    search_count = models.IntegerField(default=0)
    def __str__(self):
        return f"{self.user_id} - {self.content_id}"
    class Meta:
        unique_together = ('user_id', 'content_id')
        verbose_name_plural = "search_history"


class Favorite(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    content_id = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='favorites')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    liked = models.BooleanField(default=False)
    is_favorite = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.content_id} - {self.user_id}"
    class Meta:
        unique_together = ('content_id', 'user_id')
        verbose_name_plural = "favorites"

        verbose_name = "favorite"


class ContentScore(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    content_id = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='content_scores')
    score = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.content_id} - {self.score}"
    class Meta:
        verbose_name_plural = "content_scores"
        unique_together = ('content_id',)




# class Recommendation(models.Model):
#     RECOMMENDATION_TYPES = [
#         ('Trending', 'Trending'),
#         ('Top Rated', 'Top Rated'),
#         ('New Release', 'New Release'),
#         ('Personalized', 'Personalized'),
#     ]
#
#     content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='recommendations')
#     recommendation_type = models.CharField(max_length=50, choices=RECOMMENDATION_TYPES)
#     trending_score = models.FloatField(default=0)
#     updated_at = models.DateTimeField(auto_now=True)
