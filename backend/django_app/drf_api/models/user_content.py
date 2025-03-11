import uuid

from .all_content import Content, Genre
from .user_models import User
from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import timedelta



class SearchHistory(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)



class VisitCount(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    content_id = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='visit_counts')
    visit_count = models.IntegerField(default=0)
    last_visited = models.DateTimeField(auto_now=True)


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
