from django_filters import rest_framework as django_filters
from orders.models import Order


class OrderFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(lookup_expr='exact')
    is_paid = django_filters.BooleanFilter()
    date_from = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    date_to = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Order
        fields = ['status', 'is_paid', 'date_from', 'date_to']
