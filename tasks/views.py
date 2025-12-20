from rest_framework import generics, filters, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView

from .models import Task, Category
from .serializers import TaskSerializer, CategorySerializer
from rest_framework import status
from rest_framework.permissions import AllowAny



# -------------------------
# Task List + Create
# -------------------------
class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = {
        'priority': ['exact'],
        'completed': ['exact'],
        'due_date': ['exact', 'gte', 'lte'],
    }

    search_fields = ['title', 'description']
    ordering_fields = ['priority', 'due_date', 'created_at']
    ordering = ['created_at']

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# -------------------------
# Retrieve, Update, Delete
# -------------------------
class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


# -------------------------
# Mark Task as Completed
# -------------------------
class TaskCompleteView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            task = Task.objects.get(pk=pk, user=request.user)
        except Task.DoesNotExist:
            return Response(
                {"detail": "Task not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        task.completed = True
        task.save()

        return Response(
            {"message": "Task marked as completed"},
            status=status.HTTP_200_OK
        )


# -------------------------
# Categories
# -------------------------
class CategoryListCreateView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    ordering = ['name']

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)



class TaskCompleteView(APIView):
    permission_classes = [AllowAny]

    def patch(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response(
                {"error": "Task not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Toggle completion status
        task.completed = not task.completed
        task.save()

        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)
