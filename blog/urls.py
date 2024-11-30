from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post-list'),
    path('search/', views.search, name='search'),
    path('<slug:slug>/', views.post_detail, name='post-detail'),
    path('category/<slug:slug>/', views.category_detail, name='category-detail'),
    path('<slug:slug>/comment/', views.add_comment, name='add-comment'),
]
