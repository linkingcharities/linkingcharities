from rest_framework import serializers
from testapp.models import Charity

class CharitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Charity
        fields = ('id', 'name', 'registered_id', 'description')
