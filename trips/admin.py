from django.contrib import admin
from .models import Destination, DestinationImage, Inquiry

# Register your models here.

class DestinationImageInline(admin.TabularInline):
    model = DestinationImage
    extra = 1

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('title', 'trip_type', 'price', 'duration', 'featured')
    list_filter = ('trip_type', 'featured')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [DestinationImageInline]

@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'destination', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'message')
