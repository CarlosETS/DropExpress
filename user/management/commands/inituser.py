# inituser.py
from django.core.management.base import BaseCommand
from user.forms.register_form import CustomUserForm
from user.models import CustomUser

class Command(BaseCommand):
    def handle(self, *args, **options):
        print('Initializing a regular user account...')
        
        form_data = {
            'username': 'regular_user',
            'password': 'RegularUser!12345',
            'name': 'Regular User',
            'email': 'regular_user@gmail.com',
            'cell': '(XX) XXXX-XXXX',
            'cep': 'XXXXX-XXX',
            'address': 'Street ABC',
            'complement': 'Apt 123',
            'district': 'XYZ',
            'city': 'Example City',
            'is_active': True,
            'is_adimin': False
        }

        form = CustomUserForm(form_data)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()
            print('Regular user created successfully.')
        else:
            print('Form is not valid. Regular user not created.')
            print(form.errors)
