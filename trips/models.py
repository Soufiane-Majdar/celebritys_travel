from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField

# Create your models here.

class Destination(models.Model):
    TRIP_TYPES = (
        ('adventure', 'Adventure'),
        ('cultural', 'Cultural'),
        ('desert', 'Desert Safari'),
        ('nature', 'Nature'),
        ('umrah', 'Umrah'),
    )
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = RichTextField()
    location = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discount = models.PositiveIntegerField(null=True, blank=True)
    duration = models.PositiveIntegerField(help_text="Duration in days")
    max_group_size = models.PositiveIntegerField(default=15)
    rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    trip_type = models.CharField(max_length=20, choices=TRIP_TYPES)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('trips:trip-detail', kwargs={'slug': self.slug})
    
    def save(self, *args, **kwargs):
        # Calculate original price and discount if not set
        if self.discount and not self.original_price:
            self.original_price = self.price / (1 - self.discount/100)
        elif self.original_price and not self.discount:
            self.discount = int((1 - self.price/self.original_price) * 100)
        super().save(*args, **kwargs)

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
