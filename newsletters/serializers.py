from rest_framework.serializers import ModelSerializer

from newsletters.models import Newsletter, Tag


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class TagShowSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'slug']


class NewsletterSerializer(ModelSerializer):
    tags = TagShowSerializer(many=True, read_only=True)

    class Meta:
        model = Newsletter
        fields = ['id', 'name', 'description', 'image_url', 'tags', 'votes', 'published', 'subscribers', 'created_by']


class NewsletterCreateSerializer(ModelSerializer):
    class Meta:
        model = Newsletter
        fields = '__all__'
