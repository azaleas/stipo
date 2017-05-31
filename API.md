# Search Places

 * URL: /api/v1/places/searchplaces/
 * HTTP Method: POST
 
## Example Request

    {
	    "location": Amsterdam,
	}
    
## Example Response

    [
	    {
			"id": 18,
			"name": "Arendsnest",
			"location": "Amsterdam",
			"rating": "4.5",
			"url": "https://www.yelp.com/biz/arendsnest-amsterdam-2?adjust_creative=jos-y9cCoGyrA2dE3OOVrg&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=jos-y9cCoGyrA2dE3OOVrg",
			"image_url": "https://s3-media1.fl.yelpcdn.com/bphoto/FurcfTuqaYBv_q34bGTK5g/o.jpg",
			"attends": [
				{
					"user": 3,
					"is_going": true,
					"time": 1496205599000.0
				},
				{
					"user": 4,
					"is_going": false,
					"time": 1496205150000.0
				},
				...
			]
		},
	    ...
	]
	

# Attend

 * URL: /api/v1/places/1/attend
 * HTTP Method: POST

## Example Request

	{
	    "is_going": true,
	}
	
## Example Response
	HTTP 200 OK
	
	{
		"Saved"
	}
   
## Authentication
http://django-rest-auth.readthedocs.io/en/latest/api_endpoints.html

