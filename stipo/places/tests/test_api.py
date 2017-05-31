import json
from unittest.mock import patch, MagicMock

from django.contrib.auth.models import User

from rest_framework.test import APITestCase

from places.models import Facility, Attend, YelpToken


yelp_results = r'''{
    "businesses": [
        {
          "rating": 4,
          "price": "$",
          "phone": "+14152520800",
          "id": "four-barrel-coffee-san-francisco",
          "is_closed": false,
          "categories": [
            {
              "alias": "coffee",
              "title": "Coffee & Tea"
            }
          ],
          "review_count": 1738,
          "name": "Four Barrel Coffee",
          "url": "https://www.yelp.com/biz/four-barrel-coffee-san-francisco",
          "coordinates": {
            "latitude": 37.7670169511878,
            "longitude": -122.42184275
          },
          "image_url": "http://s3-media2.fl.yelpcdn.com/bphoto/MmgtASP3l_t4tPCL1iAsCg/o.jpg",
          "location": {
            "city": "San Francisco",
            "country": "US",
            "address2": "",
            "address3": "",
            "state": "CA",
            "address1": "375 Valencia St",
            "zip_code": "94103"
          },
          "distance": 1604.23,
          "transactions": ["pickup", "delivery"]
        }
    ]
}'''

yelp_results_json = json.loads(yelp_results)

yelp_results_not_found = r'''{
    "error": {
        "code": "LOCATION_NOT_FOUND", 
        "description": "Could not execute search, try specifying a more exact location."
    }
}'''

yelp_results_not_found_json = json.loads(yelp_results_not_found)

class PlacesAPITestCase(APITestCase):

    def setUp(self):

        self.user1 = User.objects.create_user(
            username = "testuser1",
            email = "test@test.com",
            password = "testuser"
        )

        self.user2 = User.objects.create_user(
            username = "testuser2",
            email = "test1@test.com",
            password = "testuser"
        )

        self.facility1 = Facility.objects.create(
            yelp_id = "Some_nice_place",
            name = "Some nice place",
            rating = 5,
            location = "Dubai",
            url = "http://someurl.com/some_nice_place",
            image_url = "http://someurl.com/some_nice_place_image.jpg",
        )

        self.facility2 = Facility.objects.create(
            yelp_id = "Some_nice_place2",
            name = "Some nice place 2",
            rating = 5,
            location = "Dubai",
            url = "http://someurl.com/some_nice_place2",
            image_url = "http://someurl.com/some_nice_place_image2.jpg",
        )

        self.attend1 = Attend.objects.create(
            attender = self.user1,
            facility = self.facility1,
            is_going = True,
        )

        self.attend2 = Attend.objects.create(
            attender = self.user1,
            facility = self.facility2,
            is_going = True,
        )

        self.attend3 = Attend.objects.create(
            attender = self.user2,
            facility = self.facility1,
            is_going = True,
        )

        self.attend4 = Attend.objects.create(
            attender = self.user2,
            facility = self.facility2,
            is_going = True,
        )

        self.yelpToken = YelpToken.objects.create(
            token = "123456789"
        )


    # HELPER FUNCTIONS

    def login(self, username):
        user = User.objects.get(username=username)
        self.client.force_authenticate(user=user)

    # TEST FUNCTIONS

    def test_search_by_location(self):
        """
        Test that we can get facilities list for a given location
        """
        response = self.client.post(
            '/api/v1/places/searchplaces/', 
            data={
                "location": "Dubai",
            },
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['name'], self.facility1.name)

    @patch('places.yelp.obtain_bearer_token', "123456789")
    @patch('places.yelp.search')
    def test_search_by_location_api_fetch(self, mock_yelp_search):
        """
        Test API fetch from Yelp API
        """
        mock_yelp_search.status_code = 200
        mock_yelp_search.return_value = yelp_results_json
        response = self.client.post(
            '/api/v1/places/searchplaces/', 
            data={
                "location": "San Francisco",
            },
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        facilities = Facility.objects.filter(location="San Francisco")
        self.assertEqual(len(facilities), 1)

    @patch('places.yelp.obtain_bearer_token', "123456789")
    @patch('places.yelp.search')
    def test_search_location_not_found_api_fetch(self, mock_yelp_search):
        """
        Test API fetch from Yelp API, not found location
        """
        mock_yelp_search.status_code = 404
        mock_yelp_search.return_value = yelp_results_not_found_json
        response = self.client.post(
            '/api/v1/places/searchplaces/', 
            data={
                "location": "Dubai1",
            },
            format='json'
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, "location not found")

    def test_attend(self):
        """
        Test that we attend given facility
        """
        self.login(self.user1.username)
        response = self.client.post(
            '/api/v1/places/1/attend/', 
            data={
                "is_going": "true",
            },
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, "saved")

        attends = Attend.objects.latest('id')
        self.assertEqual(attends.attender.username, self.user1.username)

    def test_cant_attend_if_not_logged_in(self):
        """
        Test that we attend given facility
        """
        response = self.client.post(
            '/api/v1/places/1/attend/', 
            data={
                "is_going": "true",
            },
            format='json'
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['detail'], "Authentication credentials were not provided.")
