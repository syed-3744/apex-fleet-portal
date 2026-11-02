from django.urls import path
from . import views

urlpatterns = [
    path('', views.car_catalog_view, name='car_catalog'),
    path('api/trip-matcher/', views.trip_matcher_api, name='trip_matcher_api'),
    path('reserve/<int:car_id>/', views.reserve_car_view, name='reserve_car'),
]