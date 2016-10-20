from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from django.db.models import Q

from rest_framework.serializers import (
    HyperlinkedIdentityField,
    ModelSerializer,
    SerializerMethodField,
    ValidationError,
    CharField,
    EmailField,
)

User = get_user_model()

class AccountCreateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'email',
        ]
        extra_kwargs = {"password" : {"write_only" : True} }
    
    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        user_obj = User(
            username = username,
            email = email
        )
        user_obj.set_password(password)
        user_obj.save()
        return validated_data

class AccountLoginSerializer(ModelSerializer):
    token = CharField(allow_blank=True, read_only=True)
    username = CharField(required=True)
    email = EmailField(label='Email Address')
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'token',
        ]
        extra_kwargs = {"password": {"write_only": True} }
    def validate(self, data):
        user_obj = None
        username = data.get("username", None)
        password = data.get("password")
        if not username:
            raise ValidationError("Username is required.")
        user = User.objects.filter(
            Q(username=username)
        ).distinct()
        user = user.exclude(email__isnull=True).exclude(email__iexact='')
        if user.exists() and user.count() == 1:
            user_obj = user.first()
        else:
            raise ValidationError("This username is not valid.")
        
        if user_obj:
            if not user_obj.check_password(password):
                raise ValidationError("Incorrect password.")

        data["token"] = "token" 

        return data
