# https://github.com/Yelp/yelp-fusion/blob/master/fusion/python/sample.py

import argparse
import json
import pprint
import requests
import sys
import urllib

from urllib.error import HTTPError
from urllib.parse import quote
from urllib.parse import urlencode
from datetime import date, timedelta

from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

from .models import YelpToken

# settings.YELP_CLIENT_ID
# settings.YELP_CLIENT_SECRET

# API constants, you shouldn't have to change these.
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.
TOKEN_PATH = '/oauth2/token'
GRANT_TYPE = 'client_credentials'

SEARCH_LIMIT = 20

def obtain_bearer_token(host=API_HOST, path=TOKEN_PATH):
    """Given a bearer token, send a GET request to the API.
    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        url_params (dict): An optional set of query parameters in the request.
    Returns:
        str: OAuth bearer token, obtained using client_id and client_secret.
    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    CLIENT_ID = settings.YELP_CLIENT_ID
    CLIENT_SECRET = settings.YELP_CLIENT_SECRET
    data = urlencode({
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': GRANT_TYPE,
    })
    headers = {
        'content-type': 'application/x-www-form-urlencoded',
    }
    response = requests.request('POST', url, data=data, headers=headers)
    bearer_token = response.json()['access_token']
    YelpToken.objects.update_or_create(token=bearer_token)
    return bearer_token

def search(bearer_token, location):
    """Query the Search API by a search location.
    Args:
        location (str): The search location passed to the API.
    Returns:
        dict: The JSON response from the request.
    """

    url_params = {
        'location': location.replace(' ', '+'),
        'limit': SEARCH_LIMIT
    }
    return request(API_HOST, SEARCH_PATH, bearer_token, url_params=url_params)

def query_api(location):
    """Queries the API by the input values from the user.
    Args:
        location (str): The location of the business to query.
    """
    try:
        """
        Yelp token should be updated every 180 days
        """
        date_cached = date.today() - timedelta(days=180)
        bearer_token_object = YelpToken.objects.get(updated_date__gte=date_cached)
        bearer_token = bearer_token_object.token
    except ObjectDoesNotExist:
        bearer_token = obtain_bearer_token()
    
    print('bearer\n', bearer_token)

    # response = search(bearer_token, location)

    # print('response\n', response)