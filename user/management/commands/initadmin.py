# initadmin.py
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from user.forms.register_form import CustomUserForm
from user.models import CustomUser

class Command(BaseCommand):
    def handle(self, *args, **options):
        if CustomUser.objects.count() == 0:
            print('Creating account for %s (%s)' % ('dev', 'dev@gmail.com'))
            
            form_data = {
                'username': 'dev',
                'password': 'Dev!12345',
                'name': 'dev',
                'email': 'dev@gmail.com',
                'cell': '(45) 99566-7232',
                'cep': '85419-203',
                'address': 'Rua Pato Branco',
                'complement': 'Prédio',
                'district': 'PR',
                'city': 'Toledo',
                'is_active': True
            }

            form = CustomUserForm(form_data)

            if form.is_valid():
                user = form.save(commit=False)
                user.is_active = True
                user.save()
                print('User created successfully.')
            else:
                print('Form is not valid. User not created.')
                print(form.errors)
        else:
            print('Admin accounts can only be initialized if no Accounts exist')
