
from django.urls import path
from demo_app import views

urlpatterns = [
    path('', views.demo_app_drf),
    path('demo-version/', views.demo_version),
    path('custom-version/', views.DemoView.as_view()),
    path('another-custom-version/', views.AnotherView.as_view()),
    path('hello-world/', views.hello_world),
    path('apiview-class/', views.DemoAPIView.as_view()),
]
