from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Destination, Inquiry

def trip_list(request):
    trips = Destination.objects.all().order_by('-created_at')
    paginator = Paginator(trips, 9)  # Show 9 trips per page
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'trips/trip_list.html', context)

def trip_detail(request, slug):
    trip = get_object_or_404(Destination, slug=slug)
    related_trips = Destination.objects.filter(
        trip_type=trip.trip_type
    ).exclude(id=trip.id)[:3]
    
    context = {
        'trip': trip,
        'related_trips': related_trips,
    }
    return render(request, 'trips/trip_detail.html', context)

def trip_category(request, trip_type):
    trips = Destination.objects.filter(trip_type=trip_type).order_by('-created_at')
    paginator = Paginator(trips, 9)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'trip_type': trip_type,
    }
    return render(request, 'trips/trip_category.html', context)

def submit_inquiry(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        destination_id = request.POST.get('destination')
        message = request.POST.get('message')
        
        try:
            destination = None
            if destination_id:
                destination = Destination.objects.get(id=destination_id)
            
            Inquiry.objects.create(
                name=name,
                email=email,
                phone=phone,
                destination=destination,
                message=message
            )
            messages.success(request, "Your inquiry has been submitted successfully!")
        except Exception as e:
            messages.error(request, "There was an error submitting your inquiry. Please try again.")
    
    return redirect(request.META.get('HTTP_REFERER', 'trips:trip-list'))

def umrah_services(request):
    return render(request, 'trips/umrah_services.html')
