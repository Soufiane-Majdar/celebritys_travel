from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from trips.models import Destination
from blog.models import Post
from .models import Testimonial, FAQ, Newsletter

def home(request):
    featured_trips = Destination.objects.filter(featured=True)[:6]
    latest_posts = Post.objects.all()[:3]
    
    context = {
        'featured_trips': featured_trips,
        'latest_posts': latest_posts,
    }
    return render(request, 'core/home.html', context)

def about(request):
    testimonials = Testimonial.objects.filter(active=True)
    context = {
        'testimonials': testimonials,
    }
    return render(request, 'core/about.html', context)

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Send email
        email_message = f"Name: {name}\nEmail: {email}\nMessage: {message}"
        try:
            send_mail(
                subject=f"Contact Form: {subject}",
                message=email_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_EMAIL],
                fail_silently=False,
            )
            messages.success(request, "Your message has been sent successfully!")
        except Exception as e:
            messages.error(request, "There was an error sending your message. Please try again later.")
        
        return redirect('core:contact')
    
    return render(request, 'core/contact.html')

def newsletter_signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            # Check if email already exists
            if not Newsletter.objects.filter(email=email).exists():
                Newsletter.objects.create(email=email)
                messages.success(request, "Thank you for subscribing to our newsletter!")
            else:
                messages.info(request, "You are already subscribed to our newsletter.")
        else:
            messages.error(request, "Please provide a valid email address.")
    
    return redirect(request.META.get('HTTP_REFERER', 'core:home'))

def faqs(request):
    faqs_by_category = {}
    categories = ['general', 'trips', 'umrah', 'booking']
    
    for category in categories:
        faqs_by_category[category] = FAQ.objects.filter(
            category=category,
            active=True
        ).order_by('order')
    
    context = {
        'faqs_by_category': faqs_by_category,
        'categories': categories,
    }
    return render(request, 'core/faqs.html', context)
