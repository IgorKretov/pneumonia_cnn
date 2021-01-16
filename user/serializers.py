from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'}
    )

    def validate(self, attrs):
        user = authenticate(
            username=attrs['email'],
            password=attrs['password'])

        if not user:
            raise serializers.ValidationError(
                '이메일 또는 비밀번호가 틀렸습니다.'
            )

        return {'user': user}


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'password', 'name', 'address')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'},
                'min_length': 6,
            },
            'name': {'required': True}
        }

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)


class UserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('email', 'name', 'address')
        extra_kwargs = {
            'email': {'read_only': True},
            'name': {'required': True}
        }

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        return user


class PasswordChangeSerializer(serializers.Serializer):
    model = get_user_model()
    current_password = serializers.CharField(
        required=True,
        style={'input_type': 'password'}
    )
    new_password = serializers.CharField(
        required=True,
        min_length=6,
        style={'input_type': 'password'}
    )

    def check_current_password(self, user, current_password):
        if not user.check_password(current_password):
            raise serializers.ValidationError('현재 비밀번호가 일치하지 않습니다.')

    def change_password(self, user, current_password, new_password):
        self.check_current_password(user, current_password)
        user.set_password(new_password)
        user.save()
