from django.urls import path
from . import views

app_name = 'trips'

urlpatterns = [
    path('', views.trip_list, name='trip-list'),
    path('search/', views.search, name='search'),
    path('<slug:slug>/', views.trip_detail, name='trip-detail'),
    path('category/<str:trip_type>/', views.trip_category, name='trip-category'),
    path('inquiry/submit/', views.submit_inquiry, name='submit-inquiry'),
    path('umrah/', views.umrah_services, name='umrah-services'),
]
