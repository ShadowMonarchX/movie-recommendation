from django.contrib import admin
from .models.all_content import *

@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('title','rating')
    list_filter = ('rating',)
    search_fields = ('title', 'description')
    ordering = ('title', 'rating')
    model = Content

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('name',)
    ordering = ('name',)
    model = Language

@admin.register(ContentLanguage)
class ContentLanguageAdmin(admin.ModelAdmin):
    list_display = ('content', 'language')
    list_filter = ('language',)
    search_fields = ('content__title', 'language__name')
    ordering = ('content', 'language')
    model = ContentLanguage

@admin.register(Genre)
class GenerAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)
    ordering = ('name',)
    model = Genre

@admin.register(ContentGenre)
class ContentGenreAdmin(admin.ModelAdmin):
    model = ContentGenre

# @admin.register(UserSession)
# class UserSessionAdmin(admin.ModelAdmin):
#     list_display = ('session_id', 'ip_address', 'last_seen', 'created_at')
#     search_fields = ('session_id', 'ip_address')
#
# @admin.register(SearchHistory)
# class SearchHistoryAdmin(admin.ModelAdmin):
#     list_display = ('session', 'search_term', 'search_count', 'searched_at')
#     search_fields = ('search_term',)
#     list_filter = ('searched_at',)
#
# @admin.register(VisitCount)
# class VisitCountAdmin(admin.ModelAdmin):
#     list_display = ('session', 'content', 'visit_count', 'last_visited')
#     search_fields = ('session__session_id', 'content__title')
#     list_filter = ('last_visited',)
#
# @admin.register(Recommendation)
# class RecommendationAdmin(admin.ModelAdmin):
#     list_display = ('session', 'content', 'recommendation_type', 'trending_score', 'updated_at')
#     list_filter = ('recommendation_type',)
#     search_fields = ('content__title',)