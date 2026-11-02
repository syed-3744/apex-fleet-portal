from django.core.management.base import BaseCommand
from fleet.models import Car

class Command(BaseCommand):
    help = 'Populates the database with verified international performance cars'

    def handle(self, *args, **kwargs):
        cars_data = [
            {
                "brand": "Porsche",
                "model_name": "911 GT3 RS",
                "tagline": "Naturally Aspirated Track Weapon",
                "category": "LUXURY",
                "daily_rate": 24999.00,
                "seating_capacity": 2,
                "luggage_capacity": 1,
                "transmission": "AUTOMATIC",
                "fuel_type": "PETROL",
                "horsepower": 518,
                "top_speed_kmh": 296,
                "terrain_suitability": "Smooth Circuits, Mountain Switchbacks, Dry Tarmac",
                "image_url": "https://images.unsplash.com/photo-1614162692292-7ac56d7f7f1e?auto=format&fit=crop&w=1200&q=80",
                "engine_rev_url": ""
            },
            {
                "brand": "Ford",
                "model_name": "Mustang GT Fastback",
                "tagline": "Pure American V8 Muscle",
                "category": "LUXURY",
                "daily_rate": 11500.00,
                "seating_capacity": 2,
                "luggage_capacity": 2,
                "transmission": "AUTOMATIC",
                "fuel_type": "PETROL",
                "horsepower": 450,
                "top_speed_kmh": 250,
                "terrain_suitability": "Open Coastlines, Straight Highways, Drag Strips",
                "image_url": "https://images.unsplash.com/photo-1584345604476-8ec5e12e42dd?auto=format&fit=crop&w=1200&q=80",
                "engine_rev_url": ""
            },
            {
                "brand": "Mercedes-AMG",
                "model_name": "G 63",
                "tagline": "Twin-Turbo V8 Boxy Titan",
                "category": "LUXURY",
                "daily_rate": 22000.00,
                "seating_capacity": 5,
                "luggage_capacity": 4,
                "transmission": "AUTOMATIC",
                "fuel_type": "PETROL",
                "horsepower": 577,
                "top_speed_kmh": 240,
                "terrain_suitability": "Desert Dunes, Rocky Terrain, VIP City Boulevards",
                "image_url": "https://images.unsplash.com/photo-1520031441872-265e4ff70366?auto=format&fit=crop&w=1200&q=80",
                "engine_rev_url": ""
            },
            {
                "brand": "BMW",
                "model_name": "M4 Competition",
                "tagline": "Twin-Turbo Inline-6 Precision Drift Machine",
                "category": "LUXURY",
                "daily_rate": 14500.00,
                "seating_capacity": 4,
                "luggage_capacity": 3,
                "transmission": "AUTOMATIC",
                "fuel_type": "PETROL",
                "horsepower": 503,
                "top_speed_kmh": 290,
                "terrain_suitability": "Expressways, Curved Mountain Passes, Track Days",
                "image_url": "https://images.unsplash.com/photo-1555215695-3004980ad54e?auto=format&fit=crop&w=1200&q=80",
                "engine_rev_url": ""
            },
            {
                "brand": "Audi",
                "model_name": "RS6 Avant",
                "tagline": "The Ultimate 600 HP Super Wagon",
                "category": "SEDAN",
                "daily_rate": 17500.00,
                "seating_capacity": 2,
                "luggage_capacity": 2,
                "transmission": "AUTOMATIC",
                "fuel_type": "PETROL",
                "horsepower": 591,
                "top_speed_kmh": 305,
                "terrain_suitability": "Autobahn Touring, Snow & Rain Quattro Drives, Long Road Trips",
                "image_url": "https://images.unsplash.com/photo-1603584173870-7f23fdae1b7a?auto=format&fit=crop&w=1200&q=80",
                "engine_rev_url": ""
            },
            {
                "brand": "Range Rover",
                "model_name": "Sport V6 Supercharged",
                "tagline": "Unstoppable Heritage Expedition SUV",
                "category": "SUV",
                "daily_rate": 16000.00,
                "seating_capacity": 5,
                "luggage_capacity": 4,
                "transmission": "AUTOMATIC",
                "fuel_type": "PETROL",
                "horsepower": 518,
                "top_speed_kmh": 240,
                "terrain_suitability": "Deep Mud, River Crossings, Alpine Snow, Remote Expeditions",
                "image_url": "https://images.unsplash.com/photo-1563720223185-11003d516935?auto=format&fit=crop&w=1200&q=80",
                "engine_rev_url": ""
            },
            {
                "brand": "Ford",
                "model_name": "Expedition Limited",
                "tagline": "Open-Air Trail Rated Crawler",
                "category": "SUV",
                "daily_rate": 7500.00,
                "seating_capacity": 7,
                "luggage_capacity": 5,
                "transmission": "AUTOMATIC",
                "fuel_type": "PETROL",
                "horsepower": 268,
                "top_speed_kmh": 180,
                "terrain_suitability": "Boulders, Sand Dunes, Forest Trails, Off-Grid Camping",
                "image_url": "https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?auto=format&fit=crop&w=1200&q=80",
                "engine_rev_url": ""
            },
            {
                "brand": "Tesla",
                "model_name": "Model S Plaid",
                "tagline": "1020 HP Tri-Motor Electric Hyper-Sedan",
                "category": "SEDAN",
                "daily_rate": 13999.00,
                "seating_capacity": 4,
                "luggage_capacity": 4,
                "transmission": "AUTOMATIC",
                "fuel_type": "EV",
                "horsepower": 1020,
                "top_speed_kmh": 322,
                "terrain_suitability": "City Stealth, Interstate Autopilot Cruising, Instant Acceleration",
                "image_url": "https://images.unsplash.com/photo-1536700503339-1e4b06520771?auto=format&fit=crop&w=1200&q=80",
                "engine_rev_url": ""
            },
            {
                "brand": "Mercedes-Benz",
                "model_name": "AMG GT R",
                "tagline": "Twin-Turbo VR38DETT Godzilla",
                "category": "LUXURY",
                "daily_rate": 18500.00,
                "seating_capacity": 2,
                "luggage_capacity": 2,
                "transmission": "AUTOMATIC",
                "fuel_type": "PETROL",
                "horsepower": 600,
                "top_speed_kmh": 330,
                "terrain_suitability": "Technical Racetracks, High-Speed Highways, Mountain Touge",
                "image_url": "https://images.unsplash.com/photo-1617814076367-b759c7d7e738?auto=format&fit=crop&w=1200&q=80",
                "engine_rev_url": ""
            },
            {
                "brand": "Porsche",
                "model_name": "911 Turbo S",
                "tagline": "Indestructible Twin-Turbo V6 King of Overlanding",
                "category": "SUV",
                "daily_rate": 15000.00,
                "seating_capacity": 2,
                "luggage_capacity": 5,
                "transmission": "AUTOMATIC",
                "fuel_type": "DIESEL",
                "horsepower": 304,
                "top_speed_kmh": 210,
                "terrain_suitability": "Cross-Country Touring, Desert Overlanding, Family Luxury Trips",
                "image_url": "https://images.unsplash.com/photo-1594502184342-2e12f877aa73?auto=format&fit=crop&w=1200&q=80",
                "engine_rev_url": ""
            }
        ]

        Car.objects.all().delete()
        for item in cars_data:
            Car.objects.create(**item)

        self.stdout.write(self.style.SUCCESS("Fleet re-seeded cleanly with working CDN images!"))