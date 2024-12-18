from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from blog import serializers
from blog import models
from rest_framework import status
from rest_framework import generics
from rest_framework import filters


# Functional views
@api_view(['GET'])
def blog_api_view(request, *args, **kwargs):
    blogs = models.Blog.objects.all()
    blog_serializer = serializers.BlogSerializer(instance=blogs, many=True)
    return Response(blog_serializer.data)

@api_view(['GET'])
def blog_custom_api_view(request, *args, **kwargs):
    blog = models.Blog.objects.all()
    blog_serializer = serializers.BlogCustom5Serializer(instance=blog, many=True)
    return Response(blog_serializer.data)


class BlogGetCreateView(APIView):

    def get(self, request):
        blogs_list = models.Blog.objects.all()
        blogs = serializers.BlogSerializer(blogs_list, many=True)
        return Response(blogs.data)
    
    def post(self, request):
        input_data = request.data
        blog = serializers.BlogSerializer(data=input_data)
        if blog.is_valid():
            blog.save()
            return Response(blog.data, status=status.HTTP_201_CREATED)
        return Response(blog.errors, status=status.HTTP_400_BAD_REQUEST)


class BlogGetUpdateView(generics.ListCreateAPIView):
    serializer_class = serializers.BlogSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['title']

    def get_queryset(self):
        blogs_queryset = models.Blog.objects.filter(id__gt=1)
        return blogs_queryset


class BlogGetUpdateFilterView(generics.ListAPIView):
    serializer_class = serializers.BlogSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['title']

    def get_queryset(self):
        blogs_queryset = models.Blog.objects.filter(id__gt=1)
        return blogs_queryset
    

def update_blog_title(request):
    blog_id = request.GET.get('id')
    blog = models.Blog.objects.get(id=blog_id)
    if request.user.has_perm("blog.update_title"):
        return HttpResponse('User has permission to update title')
    return HttpResponse('user does not have permission to update title')


# For a Role Based Access Control (RBAC) system
def check_permission(user, group_name):
    return user.groups.filter(name=group_name).exists()

@api_view(['POST'])
def blog_view(request):
    if not check_permission(request.user, 'can_view_blog'):
        return Response(status=403)
    # perform operation


