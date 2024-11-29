from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import CustomUser
from taskTeams.models import Group
import random
import string

class Command(BaseCommand):
    help = 'Seeds the database with users and groups'

    def generate_username(self, prefix, number):
        return f"{prefix}{number}"

    def generate_password(self):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

    def handle(self, *args, **kwargs):
        # More manageable numbers for testing
        num_groups = 200
        num_chiefs = 200  # Create extra chiefs
        num_members = 1000  # Create extra members
        
        self.stdout.write('Starting data seeding...')

        try:
            with transaction.atomic():
                # Step 1: Create all users first
                self.stdout.write('Creating users...')

                # Create Chiefs
                for i in range(num_chiefs):
                    username = self.generate_username('chief', i)
                    password = self.generate_password()
                    CustomUser.objects.create_user(
                        username=username,
                        email=f"{username}@clean.com",
                        password=password,
                        role='Chief'
                    )
                    self.stdout.write(f'Created chief: {username} with password: {password}')

                # Create Members
                for i in range(num_members):
                    username = self.generate_username('member', i)
                    password = self.generate_password()
                    CustomUser.objects.create_user(
                        username=username,
                        email=f"{username}@clean.com",
                        password=password,
                        role='Member'
                    )
                    self.stdout.write(f'Created member: {username} with password: {password}')

                # Step 2: Create Groups and assign users
                self.stdout.write('Creating groups...')

                # Get all available chiefs and members
                available_chiefs = list(CustomUser.objects.filter(role='Chief', group_as_chief__isnull=True))
                available_members = list(CustomUser.objects.filter(role='Member', group_as_member__isnull=True))

                # Create Groups
                for i in range(num_groups):
                    if not available_chiefs:
                        self.stdout.write('No more available chiefs!')
                        break

                    # Select and remove a chief from available pool
                    chief = random.choice(available_chiefs)
                    available_chiefs.remove(chief)

                    # Select 1-5 members for the group
                    num_members_for_group = min(random.randint(1, 5), len(available_members))
                    if num_members_for_group == 0:
                        self.stdout.write('No more available members!')
                        break

                    group_members = random.sample(available_members, num_members_for_group)
                    # Remove selected members from available pool
                    for member in group_members:
                        available_members.remove(member)

                    # Create the group
                    group = Group.objects.create(
                        name=f"Team_{i+1}",
                        specialization=random.choice(Group.SPECIALIZATION_CHOICES)[0],
                        chief=chief,
                        rating=round(random.uniform(3.0, 5.0), 1)
                    )
                    group.members.set(group_members)

                    self.stdout.write(f'''
                    Created Team_{i+1}:
                    - Chief: {chief.username}
                    - Members: {', '.join(m.username for m in group_members)}
                    - Specialization: {group.specialization}
                    ''')

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error occurred: {str(e)}'))
            raise e

        # Final statistics
        self.stdout.write(self.style.SUCCESS(f'''
        Data seeding completed successfully!
        Created:
        - {num_chiefs} chiefs
        - {num_members} members
        - {Group.objects.count()} groups
        
        Unused users:
        - Chiefs without groups: {CustomUser.objects.filter(role='Chief', group_as_chief__isnull=True).count()}
        - Members without groups: {CustomUser.objects.filter(role='Member', group_as_member__isnull=True).count()}
        '''))