from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import timedelta


class Content(models.Model):
    objects = None
    id = models.BigAutoField(primary_key=True, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    image_url = models.URLField(max_length=500 ,blank=True)
    trailer_url = models.URLField(max_length=500, blank=True)
    start_to_end_time = models.DurationField(_('Duration of movie'), blank=True, default=timedelta(hours=4))
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    release_at = models.DateTimeField(default=None, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "contents"


class Genre(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "genres"

class ContentGenre(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='genres')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='contents')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.content.title} - {self.genre.name}"

    class Meta:
        unique_together = ('content', 'genre')



class Language(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name



class ContentLanguage(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='languages')
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='contents')

    def __str__(self):
        return f"{self.content.title} - {self.language.name}"
