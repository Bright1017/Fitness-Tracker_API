import django_filters
from .models import Activity
from django.utils import timezone

class ActivityFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(
        field_name='date', 
        lookup_expr='gte',
        label='Start Date (YYYY-MM-DD)'
    )
    end_date = django_filters.DateFilter(
        field_name='date', 
        lookup_expr='lte',
        label='End Date (YYYY-MM-DD)'
    )
    
    class Meta:
        model = Activity
        fields = {
            'activity_type': ['exact'],
        }