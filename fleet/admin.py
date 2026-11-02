from django.contrib import admin
from .models import Car, Reservation

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model_name', 'daily_rate', 'is_available')
    list_filter = ('brand', 'is_available')
    search_fields = ('brand', 'model_name')

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('car', 'customer_name', 'start_date', 'end_date', 'total_price')
    list_filter = ('start_date', 'car')
    search_fields = ('customer_name', 'customer_email', 'car__model_name')