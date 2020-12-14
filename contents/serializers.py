from rest_framework import serializers
from django.db.models import Avg, Count
from django.db import transaction
from logging import getLogger, log

from contents.models import Comment, Content, Genre, Rating


logger = getLogger(__name__)


class ListContentSerializer(serializers.ModelSerializer):
    genre = serializers.CharField(source='genre.name', read_only=True)
    avg_rating = serializers.SerializerMethodField(source='get_avg_rating')
    user_who_rated_count = serializers.SerializerMethodField(source='get_user_who_rated_count')     # Count of users who rated.
    comments = serializers.SerializerMethodField(source='get_comments')

    class Meta:
        model = Content
        fields = ('uuid', 'name', 'content_type', 'genre', 'avg_rating', 'user_who_rated_count', 'comments')
        extra_kwargs = {
            'uuid': {
                'read_only': True,
            },
            'name': {
                'read_only': True,
            },
            'content_type': {
                'read_only': True,
            },
        }

    def get_avg_rating(self, obj: Content):
        return round(obj.ratings.aggregate(avg=Avg('rating')).get('avg') or 0, 2)

    def get_user_who_rated_count(self, obj: Content):
        return obj.ratings.aggregate(count=Count('user', distinct=True)).get('count', 0)

    def get_comments(self, obj: Content):
        return [k.get('text') for k in obj.comments.all().values('text')]


class AddContentSerializer(serializers.ModelSerializer):
    genre = serializers.CharField(max_length=50,  required=False)

    class Meta:
        model = Content
        fields = ('uuid', 'name', 'content_type', 'genre')
        extra_kwargs = {
            'uuid': {
                'read_only': True,
            },
            'name': {
                'required': True,
            },
            'content_type': {
                'required': True,
            },
        }

    def to_internal_value(self, data):
        data['content_type'] = data['content_type'].lower()
        return super().to_internal_value(data)

    def validate_name(self, data):
        if Content.objects.filter(name__iexact=data).exists():
            logger.debug(f"{data.lower()} already exist in DB.")
            raise serializers.ValidationError('This movie already exists in DB.')
        return data

    @transaction.atomic
    def create(self, validated_data):
        if validated_data.get('genre'):
            data = validated_data.pop('genre').lower()
            genre, is_created = Genre.objects.get_or_create(name=data, defaults={'name':data})
            validated_data['genre'] = genre
            validated_data['created_by'] = self.context['request'].user.uuid
        return Content.objects.create(**validated_data)


class AddReviewSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(required=True)
    comment = serializers.CharField(max_length=1000, required=False)
    rating = serializers.IntegerField(max_value=10, min_value=1, required=False)

    class Meta:
        model = Content
        fields = ('uuid', 'comment', 'rating')

    def validate_uuid(self, data):
        if not Content.objects.filter(uuid=data).exists():
            logger.debug(f"Content with uuid={data} does not exist.")
            raise serializers.ValidationError('Content with given uuid does not exist.')
        return data

    def validate(self, attrs):
        if not attrs.get('comment') and not attrs.get('rating'):
            raise serializers.ValidationError('Either comment or rating or both must be present.')
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        content = Content.objects.filter(uuid=validated_data['uuid']).last()

        if validated_data.get('comment'):
            comment, is_created = Comment.objects.get_or_create(content=content, user=self.context['request'].user, is_active=True,
                                                                defaults={"text":validated_data.get('comment')})

            if not is_created:
                logger.debug(f"Comment by {self.context['request'].user.uuid} for {content.name} already exists.")
                raise serializers.ValidationError(f'There is already a comment by you for {content.name}')

        if validated_data.get('rating'):
            rating, is_created = Rating.objects.get_or_create(content=content, user=self.context['request'].user,
                                                                defaults={'rating':validated_data.get('rating')})

            if not is_created:
                logger.debug(f"Rating by {self.context['request'].user.uuid} for {content.name} already exists.")
                raise serializers.ValidationError(f'You have already rated {content.name} as {rating.rating}')
        return content

    def to_representation(self, instance):
        return {
            "content_uuid": instance.uuid,
            "rating": self.validated_data['rating'],
            "comment": self.validated_data['comment']
        }