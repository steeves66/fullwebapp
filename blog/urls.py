
from django.urls import path
from blog import views

urlpatterns = [
    path('test/', views.blog_api_view),
    path('nested/', views.blog_custom_api_view),
    path('', views.BlogGetCreateView.as_view()),
    path('create-list/', views.BlogGetUpdateView.as_view()),
    path('filter/', views.BlogGetUpdateFilterView.as_view()),
]
