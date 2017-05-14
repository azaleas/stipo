from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated , AllowAny
from rest_framework.decorators import detail_route, list_route

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
            search_input = request.data['city'];
            data = {
                "search_input": search_input
            }
            return Response(search_input, status.HTTP_200_OK)