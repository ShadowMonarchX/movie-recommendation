# Generated by Django 5.1.6 on 2025-03-11 14:56

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
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
                    "start_to_end_time",
                    models.DurationField(
                        blank=True,
                        default=datetime.timedelta(seconds=14400),
                        verbose_name="Duration of movie",
                    ),
                ),
                ("rating", models.DecimalField(decimal_places=1, max_digits=3)),
                (
                    "release_at",
                    models.DateTimeField(blank=True, default=None, null=True),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name_plural": "contents",
            },
        ),
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
            name="User",
            fields=[
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "id",
                    models.BigAutoField(
                        editable=False, primary_key=True, serialize=False
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        max_length=255, unique=True, verbose_name="Email Address"
                    ),
                ),
                ("username", models.CharField(max_length=30, unique=True)),
                ("tc", models.BooleanField()),
                ("is_verified", models.BooleanField(default=False)),
                ("is_active", models.BooleanField(default=True)),
                ("is_staff", models.BooleanField(default=False)),
                ("date_joined", models.DateTimeField(auto_now_add=True)),
                ("last_login", models.DateTimeField(auto_now=True)),
                ("auth_provider", models.CharField(default="email", max_length=50)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True, related_name="custom_user_groups", to="auth.group"
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        related_name="custom_user_permissions",
                        to="auth.permission",
                    ),
                ),
            ],
            options={
                "abstract": False,
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("is_favorite", models.BooleanField(default=False)),
                ("is_liked", models.BooleanField(default=False)),
                ("updated_at", models.DateTimeField(auto_now=True)),
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
