import time
from datetime import date, timedelta, datetime

from django.utils import timezone

from ..models import Facility, Attend
from .serializers import FacilitySerializer

def get_location_from_db(location):
    """
    Returns facilities matching the location 
    and updated no more than 3 hours ago
    """
    date_cached = timezone.now() - timedelta(seconds=3*60*60)

    places = Facility.objects.filter(
        location=location.title(), 
        updated_date__gte=date_cached,
    )   

    return places

def get_location_json(places):
    """
    Get attends for last 24 hours and return cleaned facilities list with attenders
    """
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

    return json_places