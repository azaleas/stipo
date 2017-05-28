from rest_framework import serializers

from ..models import Attend, Facility, YelpToken


class AttendSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Attend
        fields = ['id', 'attender', 'facility', 
        'is_going', 'created_date']

class AttendSerializerReadOnly(serializers.ModelSerializer):
   
    class Meta:
        model = Attend
        fields = ['is_going', 'created_date']

class FacilitySerializer(serializers.ModelSerializer):

    attends = AttendSerializerReadOnly(many=True, read_only=True)

    class Meta:
        model = Facility
        fields = ['id', 'name', 'location', 'rating', 'url', 'image_url', 'attends']
        read_only_fields = ['name', 'rating', 'url', 'image_url', 'attends']

class YelpTokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = YelpToken
        fields = ['token', 'updated_date']