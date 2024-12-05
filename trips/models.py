from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField
from django.utils import timezone

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
    location = models.CharField(max_length=200, default='Morocco')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discount = models.PositiveIntegerField(null=True, blank=True)
    duration = models.PositiveIntegerField(help_text="Duration in days")
    max_group_size = models.PositiveIntegerField(default=15)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=4.5)
    trip_type = models.CharField(max_length=20, choices=TRIP_TYPES)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
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

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percentage = models.PositiveIntegerField(help_text="Discount percentage (0-100)")
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    active = models.BooleanField(default=True)
    max_uses = models.PositiveIntegerField(default=100)
    current_uses = models.PositiveIntegerField(default=0)
    trip_type = models.CharField(max_length=20, choices=Destination.TRIP_TYPES, blank=True, null=True,
                               help_text="Leave blank to apply to all trip types")
    
    def __str__(self):
        return f"{self.code} - {self.discount_percentage}% off"
    
    def is_valid(self):
        now = timezone.now()
        return (self.active and 
                self.valid_from <= now <= self.valid_to and 
                self.current_uses < self.max_uses)

class Reservation(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    )
    
    reference_number = models.CharField(max_length=20, unique=True, editable=False, default='LEGACY000000')
    destination = models.ForeignKey(Destination, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    number_of_people = models.PositiveIntegerField()
    preferred_date = models.DateField()
    special_requirements = models.TextField(blank=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    final_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Reservation {self.reference_number} - {self.destination.title}"
    
    def save(self, *args, **kwargs):
        if not self.pk:  # Only on creation
            # Generate reference number
            last_reservation = Reservation.objects.order_by('-id').first()
            last_number = int(last_reservation.reference_number[3:]) if last_reservation and last_reservation.reference_number != 'LEGACY000000' else 0
            self.reference_number = f'RES{str(last_number + 1).zfill(6)}'
            
            # Calculate prices
            self.original_price = self.destination.price * self.number_of_people
            self.final_price = self.original_price
            
            if self.coupon and self.coupon.is_valid():
                if not self.coupon.trip_type or self.coupon.trip_type == self.destination.trip_type:
                    discount = self.coupon.discount_percentage / 100
                    self.final_price = self.original_price * (1 - discount)
                    self.coupon.current_uses += 1
                    self.coupon.save()
        
        super().save(*args, **kwargs)
