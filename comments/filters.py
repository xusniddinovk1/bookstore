from django_filters import rest_framework as django_filters
from comments.models import Comment


class CommentFilter(django_filters.FilterSet):
    user = django_filters.NumberFilter(field_name='user__id')
    book = django_filters.NumberFilter(field_name='book__id')

    class Meta:
        model = Comment
        fields = ['user', 'book']
