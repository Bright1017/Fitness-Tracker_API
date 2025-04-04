from rest_framework import viewsets, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .serializers import UserSerializer, ActivitySerializer, ActivityHistorySerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser, Activity
from .permissions import IsOwnerOrAdmin, IsSelfOrAdmin
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ActivityFilter
from rest_framework.views import APIView
from rest_framework.response import Response



class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                         context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
    

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsSelfOrAdmin]

    def get_queryset(self):
        if self.request.user.is_staff:
            return CustomUser.objects.all()
        return CustomUser.objects.filter(id=self.request.user.id)
    

class ActivityViewSet(viewsets.ModelViewSet):
    serializer_class = ActivitySerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ActivityFilter
    
    def get_queryset(self):
        queryset = Activity.objects.filter(user=self.request.user)
        
        # Handle date range filtering
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        if start_date and end_date:
            queryset = queryset.filter(
                date__date__range=[start_date, end_date]
            )
            
        return queryset.order_by('-date')
    

class ActivityHistoryView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        queryset = Activity.objects.filter(user=request.user)
        filtered_queryset = ActivityFilter(request.GET, queryset=queryset).qs
        serializer = ActivityHistorySerializer(filtered_queryset, many=True)
        return Response(serializer.data)