from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from author import serializers, models


# Functional views
@api_view(['GET'])
def author_api_view(request, *args, **kwargs):
    authors = models.Author.objects.all()
    author_serializer = serializers.AuthorSerializers(instance=authors, many=True)
    return Response(author_serializer.data)