from django.contrib import admin
from drf_api.models.user_movies import Content, Episode, Language, ContentLanguage, UserSession, SearchHistory, VisitCount, Recommendation

@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'types', 'category', 'status', 'release_at', 'reting', 'ott_release_at')
    list_filter = ('types', 'category', 'status')
    search_fields = ('title', 'description')
    ordering = ('release_at',)

@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'season', 'episode_number', 'release_at', 'ott_release_at')
    list_filter = ('content', 'season')
    search_fields = ('title', 'description')

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)

@admin.register(ContentLanguage)
class ContentLanguageAdmin(admin.ModelAdmin):
    list_display = ('content', 'language')
    list_filter = ('language',)
    search_fields = ('content__title', 'language__name')

@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = ('session_id', 'ip_address', 'last_seen', 'created_at')
    search_fields = ('session_id', 'ip_address')

@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ('session', 'search_term', 'search_count', 'searched_at')
    search_fields = ('search_term',)
    list_filter = ('searched_at',)

@admin.register(VisitCount)
class VisitCountAdmin(admin.ModelAdmin):
    list_display = ('session', 'content', 'visit_count', 'last_visited')
    search_fields = ('session__session_id', 'content__title')
    list_filter = ('last_visited',)

@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ('session', 'content', 'recommendation_type', 'trending_score', 'updated_at')
    list_filter = ('recommendation_type',)
    search_fields = ('content__title',)