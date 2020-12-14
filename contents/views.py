from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from rest_framework.response import Response

from contents.models import Content, Comment, Rating
from contents.serializers import ListContentSerializer, AddContentSerializer, AddReviewSerializer
from utils.permissions import IsAdminUserOrReadOnly


class ContentView(APIView):
    permission_classes = (IsAdminUserOrReadOnly,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, *args, **kwargs):
        queryset = Content.objects.all()

        if request.query_params.get('name'):
            queryset = queryset.filter(name__icontains=request.query_params.get('name'))

        if request.query_params.get('type'):
            queryset = queryset.filter(content_type__iexact=request.query_params.get('type'))

        data = ListContentSerializer(queryset, many=True).data
        if not data:
            return Response([], status=status.HTTP_404_NOT_FOUND)
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = AddContentSerializer(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ReviewView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def post(self, request, *args, **kwargs):
        _request_data = request.data
        _request_data['uuid'] = kwargs.get('uuid')
        serializer = AddReviewSerializer(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MyReviewView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, *args, **kwargs):
        comment_qs = Comment.objects.select_related('content').filter(user=request.user)
        rating_qs = Rating.objects.select_related('content').filter(user=request.user)
        data = {
            "user_uuid": request.user.uuid,
            "comments": [
                {
                    'content_name': comment.content.name,
                    'content_type': comment.content.content_type,
                    'comment': comment.text
                }
                for comment in comment_qs
            ],
            "ratings": [
                {
                    'content_name': rating.content.name,
                    'content_type': rating.content.content_type,
                    'rating': rating.rating
                }
                for rating in rating_qs
            ]
        }
        return Response(data, status=status.HTTP_200_OK)