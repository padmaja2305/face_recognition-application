from django.contrib import admin
from .models import Attendee,AttendanceLog
from django.conf.locale.es import formats as es_formats


# Register your models here.
@admin.register(Attendee)
class AttendeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'profile_img')

@admin.register(AttendanceLog)
class AttendanceLogAdmin(admin.ModelAdmin):
    es_formats.DATETIME_FORMAT = "d M Y H:i:s"
    list_display = ('id','attendee', 'timestamp')
    list_filter = ('attendee', )
    