from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet,
    ActivityViewSet,
    CustomAuthToken,
    ActivityHistoryView
)

# Initialize router
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'activities', ActivityViewSet, basename='activity')

urlpatterns = [
    # REST framework's login/logout for browsable API
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    
    # Custom authentication endpoint
    path('auth/', CustomAuthToken.as_view(), name='api-token-auth'),
    
    # Activity history endpoint with filters
    path('activities/history/', ActivityHistoryView.as_view(), name='activity-history'),
    
    # Router URLs (must come last to avoid route conflicts)
    path('', include(router.urls)),
]