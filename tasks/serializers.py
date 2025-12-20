from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Task, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

    def create(self, validated_data):
        request = self.context.get('request')
        return Category.objects.create(
            user=request.user,
            **validated_data
        )


class TaskSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.none(),
        source='category',
        write_only=True,
        required=False
    )

    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'completed',
            'priority',
            'due_date',
            'created_at',
            'category',
            'category_id',
        ]
        read_only_fields = ['id', 'created_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            self.fields['category_id'].queryset = Category.objects.filter(user=request.user)

    def create(self, validated_data):
        request = self.context.get('request')
        return Task.objects.create(
            user=request.user,
            **validated_data
        )
