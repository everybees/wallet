from rest_framework import serializers

from accounts.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'user_type', 'password']
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        # print(validated_data)
        user = User(
            **validated_data
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
