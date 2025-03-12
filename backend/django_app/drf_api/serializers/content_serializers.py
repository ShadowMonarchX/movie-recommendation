from rest_framework import serializers
from ..models.all_content import Content


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = '__all__'


