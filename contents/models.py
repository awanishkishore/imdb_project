from django.db import models
import uuid
from model_utils.models import TimeStampedModel

from contents.choices import ContentTypeChoices
from accounts.models import User


class Genre(models.Model):

    class Meta:
        db_table = 'genre'

    uuid = models.UUIDField("UUID", default=uuid.uuid4, unique=True)
    name = models.CharField(max_length=100, null=True, db_index=True)

    def __str__(self) -> str:
        return self.name


class Content(TimeStampedModel):

    class Meta:
        db_table = 'content'

    uuid = models.UUIDField("UUID", default=uuid.uuid4, unique=True)
    name = models.CharField(max_length=200, null=True, db_index=True)
    content_type = models.CharField(choices=ContentTypeChoices.choices, max_length=50, null=True)
    genre = models.ForeignKey(Genre, related_name='movies', null=True, on_delete=models.SET_NULL)
    created_by = models.UUIDField(null=True)

    def __str__(self) -> str:
        return self.name


class Comment(TimeStampedModel):

    class Meta:
        db_table = 'comment'

    uuid = models.UUIDField("UUID", default=uuid.uuid4, unique=True)
    text = models.TextField(null=True)
    content = models.ForeignKey(Content, related_name='comments', null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='comments', null=True, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)


class Rating(TimeStampedModel):

    class Meta:
        db_table = 'rating'

    uuid = models.UUIDField("UUID", default=uuid.uuid4, unique=True)
    rating = models.PositiveIntegerField(null=True, db_index=True)
    content = models.ForeignKey(Content, related_name='ratings', null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='ratings', null=True, on_delete=models.CASCADE)