import time
from datetime import date, timedelta, datetime

from django.db.models import Q

from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated , AllowAny
from rest_framework.decorators import detail_route, list_route

from ..yelp import query_api

from ..models import Attend, Facility, YelpToken
from .serializers import AttendSerializer, \
FacilitySerializer

class PlacesViewSet(viewsets.ViewSet):
    """
    Viewset to deal with search and attend method
    """
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer
    authentication_classes = [TokenAuthentication, ]

    def list(self, request):
        return Response("Stipo - Yelp Fusion API experiment with Django/React.")

    @list_route(methods=['post', 'get'])
    def searchplaces(self, request):
        if request.method == 'GET':
            return Response('Search for location...', status.HTTP_200_OK)
        else:
            serializer = FacilitySerializer(data=request.data)
            if serializer.is_valid():
                location = request.data['location']
                """
                Check if the database have the data with given location,
                created less than 3 hours ago. If not, get the data from Yelp API.
                """
                date_cached = datetime.utcnow() - timedelta(seconds=3*60*60)
                date_attend = datetime.utcnow() - timedelta(days=1)
                places = Facility.objects.filter(
                    location=location.title(), 
                    updated_date__gte=date_cached,
                )
                if places:
                    json_places = FacilitySerializer(places, many=True)
                    for place in json_places.data[:]:
                        """
                        Filter attendes for last 24 hours
                        """
                        attends = []
                        for attend in place['attends']:
                            attend_date = datetime.strptime(
                                attend['created_date'], 
                                "%Y-%m-%dT%H:%M:%S.%fZ")
                            if attend_date >= date_attend \
                            and attend['is_going'] == True:
                                # Unix timestamp for JS (* 1000)
                                attends.append(
                                    time.mktime(attend_date.timetuple())*1000
                                )
                        place['attends'] = attends

                    return Response(json_places.data[:], status.HTTP_200_OK)
                else:
                    """
                    Request to Yelp API
                    """
                    query_api(location)
                    return Response("ok from API", status.HTTP_200_OK)                   
            else:
                return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)