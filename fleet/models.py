from django.db import models
from django.contrib.auth.models import User

class Car(models.Model):
    TRANSMISSION_CHOICES = [
        ('MANUAL', 'Manual'),
        ('AUTOMATIC', 'Automatic'),
    ]

    FUEL_CHOICES = [
        ('PETROL', 'Petrol'),
        ('DIESEL', 'Diesel'),
        ('EV', 'Electric'),
        ('HYBRID', 'Hybrid'),
    ]

    CATEGORY_CHOICES = [
        ('HATCHBACK', 'Hatchback'),
        ('SEDAN', 'Executive Sedan'),
        ('SUV', 'Adventure SUV'),
        ('LUXURY', 'Luxury Sport'),
    ]

    # Vehicle Identity
    brand = models.CharField(max_length=50)            # e.g., Mahindra, BMW, Toyota
    model_name = models.CharField(max_length=50)       # e.g., Thar 4x4, M340i, Innova Crysta
    tagline = models.CharField(max_length=150, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='SUV')

    # Core Performance & Specs
    daily_rate = models.DecimalField(max_digits=8, decimal_places=2)
    seating_capacity = models.PositiveIntegerField(default=5)
    luggage_capacity = models.PositiveIntegerField(default=2)
    transmission = models.CharField(max_length=15, choices=TRANSMISSION_CHOICES, default='MANUAL')
    fuel_type = models.CharField(max_length=15, choices=FUEL_CHOICES, default='DIESEL')
    horsepower = models.PositiveIntegerField(default=150)
    top_speed_kmh = models.PositiveIntegerField(default=160)

    # Audio & Visual Media
    engine_rev_url = models.URLField(blank=True, null=True) # Direct audio link (.mp3)
    image_url = models.URLField(blank=True, null=True)      # Direct vehicle photo link

    # AI Matching & Status
    terrain_suitability = models.CharField(max_length=120, default="City & Highway")
    is_available = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.brand} {self.model_name} ({self.category})"


class Booking(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending Confirmation'),
        ('CONFIRMED', 'Confirmed'),
        ('COMPLETED', 'Trip Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='bookings')
    start_date = models.DateField()
    end_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    booking_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking #{self.id} - {self.car.model_name} by {self.user.username}"

from django.db import models
from django.utils import timezone

class Reservation(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='reservations')
    customer_name = models.CharField(max_length=120)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20)
    start_date = models.DateField()
    end_date = models.DateField()
    total_days = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer_name} - {self.car.brand} {self.car.model_name}"
