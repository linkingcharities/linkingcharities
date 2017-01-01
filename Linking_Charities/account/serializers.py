from rest_framework import serializers
from rest_framework.serializers import *
from account.models import ( 
    DonorAccount,
    CharityAccount,
)
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework.authtoken.models import Token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [ 'username', 'password' ]
    extra_kwargs = {'password': {'write_only': True} }
  
    def create(self, validated_data):
        user = User.object.create_user(**validated_data)
        return user

class DonorAccountSerializer(serializers.ModelSerializer):
    account = UserSerializer()

    class Meta:
        model = DonorAccount
        fields = [ 'account' ]
  
    def create(self, validated_data):
        user_data = validated_data.pop('account')
        account = User.objects.create_user(**user_data)
        donorAccount = DonorAccount.objects.create(account = account, **validated_data)
        return donorAccount

class CharityAccountSerializer(serializers.ModelSerializer):
    account = UserSerializer()
    paypal = CharField(required=True)
    class Meta:
        model = CharityAccount
        fields = [ 'account', 'paypal', 'description' ]
    
    def create(self, validated_data):
        user_data = validated_data.pop('account')
        account = User.objects.create_user(**user_data)
        charityAccount = CharityAccount.objects.create(account = account, **validated_data)
        return charityAccount 

class AccountLoginSerializer(serializers.ModelSerializer):
    username = CharField(required=True)
    token = CharField(allow_blank=True, read_only=True)
    id = CharField(allow_blank=True, read_only=True)
    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'token',
            'id'
        ]
        extra_kwargs = {"password": {"write_only": True} }
    
    def validate(self, data):
        username = data.get("username", None)
        password = data.get("password")
        if not username:
            raise ValidationError("Username is required.")

        user = User.objects.filter(
            Q(username=username)
        ).distinct()
        check_donor_account = DonorAccount.objects.filter( Q(account=user) ).distinct()
        account = None
        if user.exists() and check_donor_account.exists():
            account = user.first()
        else:
            check_charity_account = CharityAccount.objects.filter( 
                Q(account=user)
            )
            if user.exists() and check_charity_account.exists():
                account = user.first()
            else:
                raise ValidationError("Username is not valid.")

        if account:
           if not account.check_password(password):
               raise ValidationError("Incorrect password.")

        token = Token.objects.get(user=account)
        data["token"] = token
        id = user.first().id
        data["id"] = id
        
        return data

