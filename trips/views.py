from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils import timezone
from django.http import JsonResponse
import json
from .models import Destination, Inquiry, Reservation, Coupon
from .forms import ReservationForm
from django.urls import reverse

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
        'category': trip_type,
    }
    return render(request, 'trips/trip_list.html', context)

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

def search(request):
    query = request.GET.get('location', '')
    category = request.GET.get('category', '')
    
    trips = Destination.objects.all()
    
    if query:
        trips = trips.filter(location__icontains=query)
    
    if category:
        trips = trips.filter(trip_type=category)
    
    paginator = Paginator(trips, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'query': query,
        'category': category,
    }
    return render(request, 'trips/trip_list.html', context)

def umrah_services(request):
    return render(request, 'trips/umrah_services.html')

def make_reservation(request, slug):
    trip = get_object_or_404(Destination, slug=slug)
    
    if request.method == 'POST':
        data = request.POST.copy()
        data['destination'] = trip.id
        form = ReservationForm(data)
        
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.destination = trip
            
            # Handle coupon if provided
            coupon_code = form.cleaned_data.get('coupon_code')
            if coupon_code:
                try:
                    coupon = Coupon.objects.get(code=coupon_code)
                    if coupon.is_valid():
                        reservation.coupon = coupon
                except Coupon.DoesNotExist:
                    pass
            
            # Save the reservation
            reservation.save()
            
            return JsonResponse({
                'success': True,
                'redirect_url': reverse('trips:reservation-confirmation', kwargs={'pk': reservation.pk})
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Please correct the form errors.',
                'errors': form.errors
            })
    
    # This should never be called since we're handling the form in trip_detail.html
    return redirect('trips:trip-detail', slug=slug)

def validate_coupon(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            code = data.get('coupon_code')
            trip_id = data.get('trip_id')
            
            try:
                coupon = Coupon.objects.get(code=code)
                trip = Destination.objects.get(id=trip_id)
                
                if not coupon.is_valid():
                    return JsonResponse({
                        'valid': False,
                        'message': 'This coupon has expired or reached maximum uses.'
                    })
                
                if coupon.trip_type and coupon.trip_type != trip.trip_type:
                    return JsonResponse({
                        'valid': False,
                        'message': 'This coupon is not valid for this type of trip.'
                    })
                
                return JsonResponse({
                    'valid': True,
                    'discount_percentage': coupon.discount_percentage,
                    'message': f'Coupon applied! You will get {coupon.discount_percentage}% off.'
                })
                
            except Coupon.DoesNotExist:
                return JsonResponse({
                    'valid': False,
                    'message': 'Invalid coupon code.'
                })
            except Destination.DoesNotExist:
                return JsonResponse({
                    'valid': False,
                    'message': 'Invalid trip.'
                })
        except json.JSONDecodeError:
            return JsonResponse({
                'valid': False,
                'message': 'Invalid JSON data.'
            })
    
    return JsonResponse({'valid': False, 'message': 'Invalid request.'})

def reservation_confirmation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    context = {
        'reservation': reservation,
    }
    return render(request, 'trips/reservation_confirmation.html', context)
