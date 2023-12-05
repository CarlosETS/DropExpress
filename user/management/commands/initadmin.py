# initadmin.py
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from user.forms import CustomUserForm
from user.models import CustomUser

class Command(BaseCommand):

    def handle(self, *args, **options):
        if CustomUser.objects.count() == 0:
            print('Creating account for %s (%s)' % ('dev', 'dev@gmail.com'))
            
            form_data = {
                'email': 'dev@gmail.com',
                'username': 'dev',
                'password': 'Dev!12345',
                'code': '9854645225',
                'office': 'gerente',
                'cell': '(45) 99566-7232',
                'cep': '85419-203',
                'address': 'Rua Pato Branco',
                'access_level': 'admin',
                'complement': 'Prédio',
                'district': 'PR',
                'city': 'Toledo',
                'rg': '32.200.815-23',
                'cpf': '811.464.820-19',
            }

            form = CustomUserForm(form_data)

            if form.is_valid():
                user = form.save(commit=False)
                user.is_active = True
                user.is_admin = True
                user.save()
                print('User created successfully.')
            else:
                print('Form is not valid. User not created.')
                print(form.errors)
        else:
            print('Admin accounts can only be initialized if no Accounts exist')
