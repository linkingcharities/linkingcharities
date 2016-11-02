from rest_framework import serializers
from charity.models import Charity


class CharitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Charity
        fields = ('id', 'name', 'register_id', 'type','description', 'target',
                  'total_income')
