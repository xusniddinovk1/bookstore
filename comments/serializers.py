from rest_framework import serializers
from comments.models import Comment
from users.models import CustomUser


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Comment
        fields = ['id', 'user', 'book', 'text', 'rating', 'created_at']