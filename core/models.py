from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.

class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='testimonials/', blank=True)
    content = models.TextField()
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.rating} stars"

class FAQ(models.Model):
    question = models.CharField(max_length=200)
    answer = RichTextField()
    category = models.CharField(max_length=50, choices=[
        ('general', 'General'),
        ('trips', 'Trips'),
        ('umrah', 'Umrah'),
        ('booking', 'Booking'),
    ])
    order = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"
    
    def __str__(self):
        return self.question

class Newsletter(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.email
