
from django.urls import path
from author import views

urlpatterns = [
    path('', views.author_api_view),
]