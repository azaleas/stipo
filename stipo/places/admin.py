from django.contrib import admin
from .models import Facility, Attend, YelpToken

# Register your models here.

class FacilityAdmin(admin.ModelAdmin):
    list_display = ['name', 'yelp_id', 'rating', 'location', 'updated_date']
    list_filter = ['created_date', 'updated_date', 'rating']

admin.site.register(Facility, FacilityAdmin)

class AttendAdmin(admin.ModelAdmin):
    list_display = ['attender', 'facility', 'is_going', 'created_date']
    list_filter = ['created_date']

admin.site.register(Attend, AttendAdmin)

class YelpTokenAdmin(admin.ModelAdmin):
    list_display = ['token', 'created_date']
    list_filter = ['created_date']

admin.site.register(YelpToken, YelpTokenAdmin)
