# from django.contrib import admin
# from django.urls import path, include
# from rest_framework.response import Response
# from rest_framework.decorators import api_view


# @api_view(["GET"])
# def api_root(request):
#     return Response({
#         "message": "Welcome to Task Management API",
#         "endpoints": {
#             "tasks": "/api/tasks/",
#             "categories": "/api/categories/",
#         }
#     })


# urlpatterns = [
#     path("admin/", admin.site.urls),

#     # API root
#     path("", api_root, name="api-root"),

#     # Tasks app
#     path("api/", include("tasks.urls")),
# ]



from django.urls import path
from .views import (
    TaskListCreateView,
    TaskDetailView,
    TaskCompleteView,
    CategoryListCreateView,
    CategoryDetailView,
)

urlpatterns = [
    path("tasks/", TaskListCreateView.as_view()),
    path("tasks/<int:pk>/", TaskDetailView.as_view()),
    path("tasks/<int:pk>/complete/", TaskCompleteView.as_view()),

    path("categories/", CategoryListCreateView.as_view()),
    path("categories/<int:pk>/", CategoryDetailView.as_view()),
]
