from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField

# Create your models here.

class Destination(models.Model):
    TRIP_TYPES = (
        ('adventure', 'Adventure'),
        ('cultural', 'Cultural'),
        ('nature', 'Nature'),
        ('umrah', 'Umrah'),
    )
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = RichTextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.PositiveIntegerField(help_text="Duration in days")
    trip_type = models.CharField(max_length=20, choices=TRIP_TYPES)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('trip-detail', kwargs={'slug': self.slug})

class DestinationImage(models.Model):
    destination = models.ForeignKey(Destination, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='destinations/')
    alt_text = models.CharField(max_length=200)
    is_feature = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.destination.title} - {self.alt_text}"

class Inquiry(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    destination = models.ForeignKey(Destination, on_delete=models.SET_NULL, null=True, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Inquiries"
    
    def __str__(self):
        return f"Inquiry from {self.name} - {self.created_at.strftime('%Y-%m-%d')}"
