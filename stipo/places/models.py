from django.db import models
from django.contrib.auth.models import User

class Facility(models.Model):
    yelp_id = models.CharField(max_length=300)
    name = models.CharField(max_length=300)
    rating = models.DecimalField(max_digits=2)
    city = models.CharField(max_length=300, db_index = True)
    url = models.UrlField(max_length=200)
    image_url = models.UrlField(max_length=200)
    created_date = models.DateTimeField(auto_now_add=True)
    #Data will be cached for 3 hours.
    updated_date = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        ordering = ['name']
        index_together = [
            ["city", "updated_date"]
        ]

    def __str__(self):
        return self.name

class Attend(models.Model):
    attender = models.ForeignKey(User, related_name='attends')
    facility = models.ForeignKey(Facility, related_name='attends')
    is_going = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_date']

class YelpToken(models.Model):
    token = models.CharField(max_length=300, db_index=True)
    created_date = models.DateTimeField(auto_now_add=True)
    #Data will be cached for 180 days.
    updated_date = models.DateTimeField(auto_now=True, db_index=True)

