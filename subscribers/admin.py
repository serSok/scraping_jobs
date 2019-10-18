from django.contrib import admin

from .models import Subscribers

class SubscribersAdmin(admin.ModelAdmin):
    class Meta:
        model = Subscribers
    list_display = ('email', 'city', 'speciality', 'is_active')
    list_editable = ['is_active']

admin.site.register(Subscribers, SubscribersAdmin)