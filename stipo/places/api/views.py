from datetime import date, timedelta

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
                date_cached = date.today() - timedelta(seconds=3*60*60)
                places = Facility.objects.filter(location=location.capitalize(), updated_date__gte=date_cached)
                if places:
                    return Response("ok from cache", status.HTTP_200_OK)
                else:
                    """
                    Request to Yelp API
                    """
                    query_api(location)
                    return Response("ok from API", status.HTTP_200_OK)                   
            else:
                return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)