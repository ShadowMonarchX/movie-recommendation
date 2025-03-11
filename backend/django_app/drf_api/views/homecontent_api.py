from rest_framework.views import APIView
from rest_framework.response import Response
from ..models.all_content import Content
from ..serializers.content_serializers import ContentSerializer


class TopAPIView(APIView):
    def get(self, request, *args, **kwargs):
        content_type = request.query_params.get('type', '0')

        try:
            content_type = int(content_type)
        except ValueError:
            return Response({"error": "Invalid content type parameter"}, status=400)


        content = Content.objects.filter(types=content_type).order_by('-rating')[:5]


        serializer = ContentSerializer(content, many=True)
        return Response(serializer.data)


class TopRecommendationCountApiView(APIView):
    def get(self, request, *args, **kwargs):
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