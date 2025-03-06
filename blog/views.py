from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from blog import serializers
from blog import models
from rest_framework import status
from rest_framework import generics
from rest_framework import filters
from cacheops import cached
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.throttling import AnonRateThrottle
from rest_framework.throttling import ScopedRateThrottle

# include logging function
from common.logging_util import log_event_


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


@cached(timeout=60*10)
def get_all_blogs(author_id):
    print('Fetching blogs from database')
    blogs = models.Blog.objects.filter(author_id=author_id)
    blogs_data = serializers.BlogSerializer(blogs, many=True).data
    return blogs_data

@api_view(['GET'])
@permission_classes([AllowAny])
def get_blogs_by_author(request):
    author_id = request.GET.get('author_id')
    # include logging event
    log_event_('get_blogs_by_author', {'author_id': author_id})
    blogs = get_all_blogs(author_id)
    return Response({'blogs': blogs})


# Use cached_as decorator whenever you want to implement 
# the auto invalidation of cached results on any data source update. 
# For example, if we want to invalidate cache on any blog table update, 
# we should use the cached_as decorator and pass the model name Blog 
# as a parameter:

from cacheops import cached_as
@cached_as(models.Blog, timeout=15*60)
def get_all_blogs(author_id):
    blogs = models.Blog.objects.filter(author_id=author_id)
    return list(blogs)


# USing throttle class
class BlogApiView(APIView):
    throttle_classes = [AnonRateThrottle]
    ...


class BlogApiView2(APIView):
    throttle_classes = [ScopedRateThrottle]
    throtlle_scope = 'blog_limit'


class BlogDetailApiView(APIView):
    throttle_classes = [ScopedRateThrottle]
    throtlle_scope = 'blog_limit'


class Blog2ApiView(APIView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'blog_2_limit'


##### Pagination part #####

def get_blog_without_pagination(request):
    blogs = models.Blog.objects.all()
    blog_data = serializers.BlogSerializer(blogs, many=True).data
    return Response(blog_data.data)


@api_view(['GET'])
def get_blog_with_pagination(request):
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 10))
    offset = (page-1) * page_size
    limit = page * page_size
    blogs = models.Blog.objects.all()[offset:limit]
    blogs_data = serializers.BlogSerializer(blogs, many=True).data
    return Response({'blogs': blogs_data})


from blog import publics
@api_view(['GET'])
def publish_blog(request):
    blog_id = request.GET.get('id')
    publics.publish_blog(blog_id)
    return Response({'status': 'success'})


# Using celery, redis and django
from fullwebapp.celery import debug_task
@api_view(['GET'])
def verify_blog(request):
    verify_word = request.GET.get('verify_word')
    debug_task.delay(f"Celery Task verification: {verify_word}")
    return Response({'status': 'success'})


# from blog import tasks
# def publish_blo(request):
#     blog = save_blog(request)
#     # publish blog code
#     tasks.send_email_to_followers.delay(blog.author_id, blog.id)


@api_view(['GET'])
def basic_req(request):
    if request.method == 'GET':
        resp = {"msg": "hello world"}
        return Response(data=resp, status=status.HTTP_200_OK)
    

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def hello_world_2(request):
    resp = {"msg": "hello world!"}
    return Response(data=resp, status=status.HTTP_200_OK)


""" 
write good error code
"""
@api_view(['GET'])
def get_blog_by_id(blog_id):
    try:
        blog = models.Blog.objects.get(id=blog_id)
    except blog.DoesNotExist:
        return Response(
            status=status.HTTP_404_NOT_FOUND,
            data={
                "error": "Blog does not exist",
                "error_code": 'BLG0012'
                }
            )
    blog_data = serializers.BlogSerializer(blog).data
    return Response(blog_data)