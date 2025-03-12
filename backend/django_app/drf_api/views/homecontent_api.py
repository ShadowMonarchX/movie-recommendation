from rest_framework.views import APIView
from rest_framework.response import Response
from ..models.all_content import Content
from ..serializers.content_serializers import ContentSerializer

class ContentListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        contents = Content.objects.all()
        serializer = ContentSerializer(contents, many=True)
        return Response(serializer.data, status=200)


class TopRecommendationCountApiView(APIView):
    def get(self):
        return None


class SearchHistoryApiView(APIView):
    def get(self, request, *args, **kwargs):
        return None


class TopRecommendationUserApiView(APIView):
    def get(self, request, *args, **kwargs):
        return None

class TopMovieApiView(APIView):
    def get(self, request, *args, **kwargs):
        return None


class TopActionApiView(APIView):
    def get(self, request, *args, **kwargs):
        return None


class TopHorrorApiView(APIView):
    def get(self, request, *args, **kwargs):
        return None


class TopLovesApiView(APIView):
    def get(self, request, *args, **kwargs):
        return None

class TopAnimeApiView(APIView):
    def get(self, request, *args, **kwargs):
        return None