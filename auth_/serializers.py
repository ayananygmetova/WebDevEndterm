import re

from rest_framework import serializers

from auth_.models import User
from common import messages


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'full_name', 'avatar']

    def get_full_name(self, obj):
        return '{} {}'.format(obj.first_name, obj.last_name)


class UserDetailsSerializer(UserSerializer):
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = UserSerializer.Meta.fields + ['username', 'website', 'birthdate', 'email', 'is_active', 'date_joined']


class RegistrationSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    def validate_first_name(self, value):
        if not value.isalpha():
            raise Exception(messages.NOT_ALL_LETTERS)
        return value

    def save(self):
        User.objects.create_user(self.validated_data['username'],
                                 self.validated_data['password'],
                                 self.validated_data['email'],
                                 self.validated_data['first_name'],
                                 self.validated_data['last_name'])


class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=100)
    new_password = serializers.CharField(max_length=100)
    new_password_repeat = serializers.CharField(max_length=100)

    def validate(self, attrs):
        if len(attrs['new_password']) < 8:
            raise Exception(messages.PASSWORD_LENGTH_SHORT)
        if attrs['new_password'] != attrs['new_password_repeat']:
            raise Exception(messages.PASSWORDS_NOT_SAME,)
        return attrs

    def change_password(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()


class ChangeDetailsSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=16)

    def validate_phone(self, value):
        if value and not re.search("[+]\d[ ]?[-]?[(]?\d{3}[)]?[ ]?[-]?\d{3}[ ]?[-]?[ ]?\d{2}[ ]?[-]?[ ]?\d{2}", value):
            raise Exception(messages.INCORRECT_PHONE_FORMAT)
        return value

    def change_details(self):
        user = self.context['request'].user
        if self.validated_data.get('phone'):
            user.profile.phone = self.validated_data['phone']
            user.profile.save()
