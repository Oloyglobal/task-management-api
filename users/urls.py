from django.urls import path
from .views import UserListCreateView, UserDetailView

urlpatterns = [
    path('users/', UserListCreateView.as_view()),
    path('users/<int:pk>/', UserDetailView.as_view()),
]
