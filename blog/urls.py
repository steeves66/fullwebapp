
from django.urls import path
from blog import views

urlpatterns = [
    path('test/', views.blog_api_view),
    path('nested/', views.blog_custom_api_view),
    path('', views.BlogGetCreateView.as_view()),
    path('create-list/', views.BlogGetUpdateView.as_view()),
    path('filter/', views.BlogGetUpdateFilterView.as_view()),
    path('cached/', views.get_blogs_by_author),
    path('paginated/', views.get_blog_with_pagination),
    path('publish/', views.publish_blog),
    path('verify/', views.verify_blog),
    path('hello-world/', views.basic_req)
]
