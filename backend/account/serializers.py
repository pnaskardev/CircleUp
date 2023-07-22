from operator import itemgetter
from rest_framework import serializers

from . models import User


class UserSerializer(serializers.ModelSerializer):

    password_1 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'password_1']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        password = attrs.get('password')
        password_1 = attrs.get('password_1')

        if password != password_1:
            raise serializers.ValidationError("Passwords should match")
        return attrs

    def create(self, validated_data):
        # print(validated_data)
        validated_data.pop('password_1')
        # print(validated_data)
        # return super().create(validated_data)
        password = validated_data.pop('password')
        user = super().create(validated_data)
        if password is not None:
            user.set_password(password)
        user.save()
        return user
