from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ActivityViewSet, CustomAuthToken

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'activities', ActivityViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', CustomAuthToken.as_view()),
]