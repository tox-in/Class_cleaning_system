from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import CustomUser
from taskTeams.models import Group
import random
from django.db import models

class Command(BaseCommand):
    help = 'Redistributes unused members to groups that have less than 5 members'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting member redistribution...')

        try:
            with transaction.atomic():
                unused_members = list(CustomUser.objects.filter(
                    role='Member', 
                    group_as_member__isnull=True
                ))
                
                if not unused_members:
                    self.stdout.write('No unused members found.')
                    return

                self.stdout.write(f'Found {len(unused_members)} unused members')

                groups = Group.objects.annotate(
                    member_count=models.Count('members')
                ).filter(member_count__lt=5)

                if not groups:
                    self.stdout.write('No groups with space for more members.')
                    return

                self.stdout.write(f'Found {groups.count()} groups with space for more members')

                for group in groups:
                    current_member_count = group.members.count()
                    spaces_available = 5 - current_member_count
                    
                    if spaces_available > 0 and unused_members:
                        members_to_add = min(spaces_available, len(unused_members))
                        
                        selected_members = random.sample(unused_members, members_to_add)
                        
                        group.members.add(*selected_members)
                        
                        for member in selected_members:
                            unused_members.remove(member)
                            
                        self.stdout.write(f'''
                        Updated {group.name}:
                        - Added {members_to_add} members
                        - New total: {group.members.count()} members
                        ''')

                        if not unused_members:
                            self.stdout.write('All unused members have been assigned!')
                            break

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error occurred: {str(e)}'))
            raise e

        remaining_unused = CustomUser.objects.filter(
            role='Member', 
            group_as_member__isnull=True
        ).count()

        self.stdout.write(self.style.SUCCESS(f'''
        Redistribution completed successfully!
        
        Final statistics:
        - Remaining unused members: {remaining_unused}
        - Groups at max capacity (5 members): {Group.objects.annotate(
            member_count=models.Count('members')
        ).filter(member_count=5).count()}
        - Groups below max capacity: {Group.objects.annotate(
            member_count=models.Count('members')
        ).filter(member_count__lt=5).count()}
        '''))