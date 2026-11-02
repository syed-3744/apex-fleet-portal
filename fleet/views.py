import json
from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings
from django.db import transaction
from django.contrib import messages
from .models import Car, Reservation

def car_catalog_view(request):
    cars = Car.objects.filter(is_available=True)
    return render(request, 'fleet/car_list.html', {'cars': cars})

@csrf_exempt
def trip_matcher_api(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method allowed'}, status=405)

    try:
        data = json.loads(request.body)
        trip_desc = data.get('trip_description', '').strip().lower()

        if not trip_desc:
            return JsonResponse({'recommendations': []})

        cars = list(Car.objects.filter(is_available=True))
        scored_cars = []

        for car in cars:
            score = 0
            reason_parts = []
            car_brand = car.brand.lower()
            car_model = car.model_name.lower()
            car_terrain = (car.terrain_suitability or '').lower()
            car_tagline = (car.tagline or '').lower()

            query_words = set(trip_desc.split())
            brand_words = set(car_brand.split())
            model_words = set(car_model.replace("(", "").replace(")", "").replace("-", " ").split())

            if brand_words & query_words or car_brand in trip_desc:
                score += 150
                reason_parts.append(f"Direct match for {car.brand}")
            
            elif model_words & query_words:
                matched_term = list(model_words & query_words)[0]
                score += 120
                reason_parts.append(f"Matches model requested ({matched_term.title()})")

            if any(term in trip_desc for term in ['family', '6 people', '7 people', 'group', 'passengers']):
                if car.seating_capacity >= 6:
                    score += 60
                    reason_parts.append(f"Spacious {car.seating_capacity}-seater cabin for groups")
                elif car.seating_capacity >= 5:
                    score += 25

            if any(term in trip_desc for term in ['hill', 'mountain', 'ghat', 'off-road', 'mud', 'trail', 'desert', 'snow', 'camping']):
                if car.category == 'SUV' or 'off-road' in car_terrain or 'trail' in car_terrain or 'overlanding' in car_terrain:
                    score += 55
                    reason_parts.append("High-clearance all-terrain chassis engineered for tough trails")

            if any(term in trip_desc for term in ['highway', 'expressway', 'track', 'fast', 'speed', 'racetrack', 'drift', 'v8']):
                if car.horsepower >= 450:
                    score += 50
                    reason_parts.append(f"Explosive {car.horsepower} HP powertrain built for high-speed cruising")

            if any(term in trip_desc for term in ['luggage', 'bags', 'suitcases', 'airport', 'touring', 'long drive']):
                if car.luggage_capacity >= 3:
                    score += 40
                    reason_parts.append(f"Generous cargo volume ({car.luggage_capacity} large suitcases)")

            if any(term in trip_desc for term in ['city', 'traffic', 'commute', 'ev', 'electric', 'quiet']):
                if car.fuel_type == 'EV':
                    score += 65
                    reason_parts.append("Zero-emission electric torque with silent, effortless city driving")
                elif car.category == 'SEDAN':
                    score += 30
                    reason_parts.append("Comfortable executive sedan ergonomics for urban driving")

            if score == 0:
                score = car.horsepower // 20
                reason_parts.append("Versatile all-around choice for open road travel")

            scored_cars.append({
                "car_id": car.id,
                "score": score,
                "match_reason": " • ".join(reason_parts)
            })

        scored_cars.sort(key=lambda x: x['score'], reverse=True)
        return JsonResponse({'recommendations': scored_cars[:3]})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def reserve_car_view(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    if request.method == 'POST':
        customer_name = request.POST.get('customer_name')
        customer_email = request.POST.get('customer_email')
        customer_phone = request.POST.get('customer_phone')
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')

        d1 = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        d2 = datetime.strptime(end_date_str, "%Y-%m-%d").date()
        total_days = (d2 - d1).days

        if total_days <= 0:
            messages.error(request, "Return date must be after pickup date.")
            return render(request, 'fleet/reserve.html', {'car': car})

        # Check for overlapping reservations on this specific car
        overlapping_booking = Reservation.objects.filter(
            car=car,
            start_date__lt=d2,
            end_date__gt=d1
        ).first()

        if overlapping_booking:
            messages.error(
                request,
                f"Unavailable! The {car.brand} {car.model_name} is already reserved from "
                f"{overlapping_booking.start_date.strftime('%d %b %Y')} to "
                f"{overlapping_booking.end_date.strftime('%d %b %Y')}. Please choose different dates."
            )
            return render(request, 'fleet/reserve.html', {'car': car})
            
        total_price = total_days * float(car.daily_rate)

        try:
            with transaction.atomic():
                Reservation.objects.create(
                    car=car,
                    customer_name=customer_name,
                    customer_email=customer_email,
                    customer_phone=customer_phone,
                    start_date=d1,
                    end_date=d2,
                    total_days=total_days,
                    total_price=total_price,
                )

                customer_subject = f"Welcome to Apex Fleet! Your {car.brand} {car.model_name} is Confirmed"
                customer_message = (
                    f"Hi {customer_name},\n\n"
                    f"Congratulations and welcome to Apex Fleet! Your reservation is officially locked in.\n"
                    f"--- BOOKING SUMMARY ---\n"
                    f"Vehicle: {car.brand} {car.model_name} ({car.tagline})\n"
                    f"Pickup Date: {d1.strftime('%d %b %Y')}\n"
                    f"Return Date: {d2.strftime('%d %b %Y')}\n"
                    f"Duration: {total_days} Day(s)\n"
                    f"Total Price: ₹{total_price:,.2f}\n"
                    f"------------------------\n\n"
                )
                
                send_mail(
                    subject=customer_subject,
                    message=customer_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[customer_email],
                    fail_silently=False,
                )

            return render(request, 'fleet/booking_success.html', {
                'car': car,
                'customer_name': customer_name,
                'total_days': total_days,
                'total_price': total_price,
            })

        except Exception as e:
            messages.error(request, "Booking failed. Please ensure your email address is valid.")
            return render(request, 'fleet/reserve.html', {'car': car})

    return render(request, 'fleet/reserve.html', {'car': car})