from django.contrib import admin
from .models import Testimonial, FAQ, Newsletter

# Register your models here.

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'rating', 'active', 'created_at')
    list_filter = ('rating', 'active')
    search_fields = ('name', 'content')

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'category', 'order', 'active')
    list_filter = ('category', 'active')
    search_fields = ('question', 'answer')
    list_editable = ('order', 'active')

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at', 'active')
    list_filter = ('active',)
    search_fields = ('email',)
