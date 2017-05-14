from rest_framework import serializers

from ..models import Attend, Facility, YelpToken


class AttendSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Attend
        fields = ['id', 'att ender', 'facility', 
        'is_going', 'created_date']

class FacilitySerializer(serializers.ModelSerializer):

    # attends = AttendSerializer(many=True)

    class Meta:
        model = Facility
        fields = ['city']

class YelpTokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = YelpToken
        fields = ['token', 'updated_date']