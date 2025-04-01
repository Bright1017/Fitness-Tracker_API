from rest_framework import serializers
from .models import User, Activity

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['id', 'activity_type', 'duration', 'distance', 
                 'distance_unit', 'calories', 'date']
        read_only_fields = ['user']

    def validate(self, data):
        activity_type = data.get('activity_type')
        distance = data.get('distance')
        distance_unit = data.get('distance_unit')

        # Validate distance requirements
        if activity_type in ['RUN', 'CYC', 'WLK', 'SWM']:
            if distance is None or distance_unit is None:
                raise serializers.ValidationError(
                    "Distance and unit are required for this activity type"
                )
        else:
            if distance is not None or distance_unit is not None:
                raise serializers.ValidationError(
                    "Distance fields should not be provided for this activity type"
                )

        return data