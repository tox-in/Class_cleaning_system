from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Count
from django.core.exceptions import ValidationError
from django.utils import timezone
from core.models import CustomUser
from taskTeams.models import Group
from reservation.models import Reservation
from datetime import datetime, timedelta
import random
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Seeds the database with clients and reservations'

    def generate_username(self, prefix, number):
        return f"{prefix}{number}"

    def validate_group_availability(self, group, cleaning_date):
        """Check if group is available on the given date"""
        existing_reservations = Reservation.objects.filter(
            assigned_group=group,
            cleaning_date=cleaning_date
        ).count()
        return existing_reservations < 3

    def get_price_by_cleaning_type(self, cleaning_type):
        """Calculate price based on cleaning type"""
        base_prices = {
            'Salon': 100,
            'Kitchen': 150,
            'Gardening': 200,
            'Backyard': 180,
            'Poultry': 250,
            'Glass': 120,
            'Laundry': 80,
        }
        return base_prices.get(cleaning_type, 100)

    def handle(self, *args, **kwargs):
        num_clients = 500
        num_reservations = 400900
        
        try:
            with transaction.atomic():
                available_groups = list(Group.objects.annotate(
                    member_count=Count('members')
                ).filter(member_count__gt=0))

                if not available_groups:
                    self.stdout.write(self.style.ERROR('No properly staffed groups found. Please run seed_data first.'))
                    return

                clients = []
                existing_clients = CustomUser.objects.filter(role='Client').count()
                
                for i in range(num_clients):
                    username = self.generate_username('client', existing_clients + i)
                    try:
                        client = CustomUser.objects.create_user(
                            username=username,
                            email=f"{username}@example.com",
                            password='password123',
                            role='Client'
                        )
                        clients.append(client)
                        logger.info(f'Created client: {username}')
                        print(client)
                    except Exception as e:
                        logger.error(f'Failed to create client {username}: {str(e)}')

                self.stdout.write(f'Created {len(clients)} clients')

                start_date = timezone.now()
                successful_reservations = 0
                failed_reservations = 0

                for i in range(num_reservations):
                    try:
                        client = random.choice(clients)
                        
                        group = random.choice(available_groups)
                        
                        days_ahead = random.randint(1, 30)
                        cleaning_date = start_date + timedelta(days=days_ahead)
                        while cleaning_date.weekday() > 4:
                            days_ahead += 1
                            cleaning_date = start_date + timedelta(days=days_ahead)

                        if not self.validate_group_availability(group, cleaning_date.date()):
                            logger.warning(f'Group {group.name} is fully booked on {cleaning_date.date()}')
                            continue

                        base_price = self.get_price_by_cleaning_type(group.specialization)
                        priority = random.choice(['High', 'Medium', 'Low'])
                        priority_multiplier = {'High': 1.3, 'Medium': 1.0, 'Low': 0.8}
                        final_price = round(base_price * priority_multiplier[priority], 2)

                        reservation = Reservation.objects.create(
                            client=client,
                            cleaning_type=group.specialization,
                            address=f"Street {random.randint(1, 100)}",
                            house_number=str(random.randint(1, 999)),
                            cleaning_date=cleaning_date.date(),
                            assigned_group=group,
                            price=final_price,
                            approved_by_client=random.choice([True, False]),
                            approved_by_admin=random.choice([True, False]),
                            priority=priority
                        )
                        
                        successful_reservations += 1
                        if successful_reservations % 10 == 0:
                            self.stdout.write(f'Created {successful_reservations} reservations')
                            
                    except ValidationError as e:
                        failed_reservations += 1
                        logger.error(f'Validation error creating reservation: {str(e)}')
                    except Exception as e:
                        failed_reservations += 1
                        logger.error(f'Unexpected error creating reservation: {str(e)}')

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error occurred: {str(e)}'))
            raise e

        self.stdout.write(self.style.SUCCESS(f'''
        Data seeding completed successfully!
        
        Statistics:
        - Created {len(clients)} clients (password: password123)
        - Successful reservations: {successful_reservations}
        - Failed reservations: {failed_reservations}
        - Total groups used: {len(available_groups)}
        
        Distribution by priority:
        - High: {Reservation.objects.filter(priority='High').count()}
        - Medium: {Reservation.objects.filter(priority='Medium').count()}
        - Low: {Reservation.objects.filter(priority='Low').count()}
        '''))