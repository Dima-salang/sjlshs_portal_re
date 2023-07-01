from django.core.management.base import BaseCommand
from ...models import StudentUser, StudentYear

class Command(BaseCommand):
    help = "Promote grade 11 student accounts and delete graduating accounts."
    def handle(self, *args, **kwargs):
        
        grade_11_year = StudentYear.objects.get(Grade_Year=11)
        grade_12_year = StudentYear.objects.get(Grade_Year=12)

        # Delete graduating accounts
        users_to_delete = StudentUser.objects.filter(grade_year=grade_12_year)
        print(f"Found {users_to_delete.count()} users to delete")
        for user in users_to_delete:
            user.delete()
            print(f"Deleted {user.last_name, user.first_name}")

        # Promote students
        StudentUser.objects.filter(grade_year=grade_11_year).update(grade_year=grade_12_year)

        print("Success! Promoted students!")

        