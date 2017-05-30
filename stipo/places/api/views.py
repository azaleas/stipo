import time
from datetime import date, timedelta, datetime

from django.db.models import Q
from django.utils import timezone

from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated , AllowAny
from rest_framework.decorators import detail_route, list_route

# For twitter
from allauth.socialaccount.providers.twitter.views import TwitterOAuthAdapter
from rest_auth.views import LoginView
from rest_auth.social_serializers import TwitterLoginSerializer

from ..yelp import query_api

from ..models import Attend, Facility
from .serializers import AttendSerializer, \
FacilitySerializer

from .helpers import get_location_from_db, get_location_json

class TwitterLogin(LoginView):
    """
    Twitter OAuth View/django-rest-auth
    """
    serializer_class = TwitterLoginSerializer
    adapter_class = TwitterOAuthAdapter

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
                places = get_location_from_db(location)              

                if places:
                    json_places = get_location_json(places)
                    return Response(json_places.data[:], status.HTTP_200_OK)
                else:
                    """
                    Request to Yelp API
                    """
                    query_status = query_api(location)
                    if query_status == "success":
                        places = get_location_from_db(location)
                        json_places = get_location_json(places)
                        return Response(json_places.data[:], status.HTTP_200_OK)
                    elif query_status == "not found":
                        return Response("location not found", status.HTTP_404_NOT_FOUND) 
                    else:
                        return Response("bad request", status.HTTP_400_BAD_REQUEST)                  
            else:
                return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    @detail_route(
        methods=['post'],
        permission_classes=[IsAuthenticated],
    )
    def attend(self, request, pk):
        try:
            if request.data['is_going'] != "" and request.data['is_going'] != None:
                is_going = request.data['is_going']
        except:
            return Response("is_going field is required", status.HTTP_400_BAD_REQUEST)

        data = {
            "attender": request.user.id,
            "facility": pk,
            "is_going": is_going
        }

        serializer = AttendSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response("saved", status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        return Response("attend", status.HTTP_200_OK)