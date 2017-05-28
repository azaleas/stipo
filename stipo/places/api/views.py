import time
from datetime import date, timedelta, datetime

from django.db.models import Q
from django.db.models import Max
from django.utils import timezone

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
                date_cached = timezone.now() - timedelta(seconds=3*60*60)

                places = Facility.objects.filter(
                    location=location.title(), 
                    updated_date__gte=date_cached,
                )                
                attends = Attend.objects.raw('''
                    SELECT attend.id, attend.facility_id, attend.attender_id, attend.created_date
                    FROM places_attend attend, (
                        SELECT attender_id, facility_id, MAX(created_date) AS max_created
                        FROM places_attend
                        GROUP BY attender_id, facility_id
                    ) AS a2
                    WHERE attend.attender_id = a2.attender_id 
                        AND attend.facility_id = a2.facility_id 
                        AND attend.created_date = a2.max_created
                ''')

                #Get all attends for 24 hours.
                date_attend = timezone.now() - timedelta(days=1)

                attends_cleaned = [elem for elem in attends if elem.created_date >= date_attend] 

                if places:
                    json_places = FacilitySerializer(places, many=True)

                    for place in json_places.data[:]:
                        attends = []
                        for attend in attends_cleaned:
                            if attend.facility.id == place['id']:
                                # Unix timestamp for JS (* 1000)
                                attends.append({
                                    'user': attend.attender.id,
                                    'is_going': attend.is_going,
                                    'time': time.mktime(attend.created_date.timetuple())*1000
                                })
                        place['attends'] = attends 
                    return Response(json_places.data[:], status.HTTP_200_OK)
                else:
                    """
                    Request to Yelp API
                    """
                    query_status = query_api(location)
                    if query_status == "success":
                        return Response("ok from API", status.HTTP_200_OK)                   
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
            if request.data['is_going']:
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