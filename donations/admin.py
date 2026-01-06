from django.contrib import admin
from .models import *
# @admin.register(DonationCenter)
class DonationCenterAdmin(admin.ModelAdmin):
    list_display = ("name", "address", "phone", "email", "town")
    search_fields = ("name", "address", "email", "town")
    list_filter = ("address", "town")
    

# @admin.register(BloodRequest)
class BloodRequestAdmin(admin.ModelAdmin):
    list_display = ("requester", "hospital_name", "blood_group", "quantity_needed", "fulfilled", "request_date")
    list_filter = ("blood_group", "fulfilled")
    search_fields = ("requester", "hospital_name")

# @admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ("donor", "center", "quantity", "date")
    list_filter = ("date", "center")
    # search_fields = ("", "center__name")


# class DonationAdmin(admin.ModelAdmin):
#     list_display = ['']

admin.site.register(Donation, DonationAdmin)
admin.site.register(BloodRequest, BloodRequestAdmin)
admin.site.register(DonationCenter, DonationCenterAdmin)
admin.site.register(DonorVerification)
admin.site.register(Question)
admin.site.register(Notification)
