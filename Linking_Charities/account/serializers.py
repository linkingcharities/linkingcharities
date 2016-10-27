from rest_framework import serializers
from account.models import ( 
    DonorAccount,
    CharityAccount,
)
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [ 'username', 'email', 'password' ]
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
   
    class Meta:
        model = CharityAccount
        fields = [ 'isCharity', 'description', 'account' ]
    
    def create(self, validated_data):
        user_data = validated_data.pop('account')
        account = User.objects.create_user(**user_data)
        charityAccount = CharityAccount.objects.create(account = account, **validated_data)
        return charityAccount 
