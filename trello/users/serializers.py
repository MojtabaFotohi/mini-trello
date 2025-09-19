from rest_framework import serializers
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'name', 'preferred_language']
        extra_kwargs = {
            'password': {'write_only': True},
            'id': {'read_only': True},
            'preferred_language': {'required': False, 'default': 'en'}
        }

    def validate_preferred_language(self, value):
        valid_languages = [lang[0] for lang in User._meta.get_field('preferred_language').choices]
        if value not in valid_languages:
            raise serializers.ValidationError("Invalid language code")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            name=validated_data.get('name', ''),
            preferred_language=validated_data.get('preferred_language', 'en')
        )
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'name', 'preferred_language']