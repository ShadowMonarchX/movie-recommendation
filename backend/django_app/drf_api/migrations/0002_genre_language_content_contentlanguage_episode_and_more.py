# Generated by Django 5.1.6 on 2025-03-05 07:29

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("drf_api", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Genre",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        editable=False, primary_key=True, serialize=False
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name_plural": "genres",
            },
        ),
        migrations.CreateModel(
            name="Language",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        editable=False, primary_key=True, serialize=False
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="Content",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        editable=False, primary_key=True, serialize=False
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("description", models.TextField()),
                ("image_url", models.URLField(blank=True, max_length=500)),
                ("trailer_url", models.URLField(blank=True, max_length=500)),
                (
                    "types",
                    models.IntegerField(
                        choices=[(0, "Movie"), (1, "Series"), (3, "TV Show")]
                    ),
                ),
                (
                    "start_to_end_time",
                    models.DurationField(
                        blank=True,
                        default=datetime.timedelta(seconds=14400),
                        verbose_name="Duration of movie",
                    ),
                ),
                ("rating", models.DecimalField(decimal_places=1, max_digits=3)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "indexes": [
                    models.Index(fields=["types"], name="drf_api_con_types_44ead8_idx")
                ],
            },
        ),
        migrations.CreateModel(
            name="ContentLanguage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "content",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="languages",
                        to="drf_api.content",
                    ),
                ),
                (
                    "language",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="contents",
                        to="drf_api.language",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Episode",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        editable=False, primary_key=True, serialize=False
                    ),
                ),
                ("season", models.IntegerField(blank=True)),
                ("episode_number", models.IntegerField()),
                ("title", models.CharField(max_length=200)),
                ("description", models.TextField()),
                ("release_at", models.DateTimeField()),
                ("ott_release_at", models.DateTimeField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "content",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="episodes",
                        to="drf_api.content",
                    ),
                ),
            ],
            options={
                "indexes": [
                    models.Index(
                        fields=["content", "season", "episode_number"],
                        name="drf_api_epi_content_a12688_idx",
                    )
                ],
            },
        ),
        migrations.CreateModel(
            name="ContentGenre",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "content",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="genres",
                        to="drf_api.content",
                    ),
                ),
                (
                    "genre",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="contents",
                        to="drf_api.genre",
                    ),
                ),
            ],
            options={
                "unique_together": {("content", "genre")},
            },
        ),
    ]
