from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    code = models.CharField(max_length=10, unique=True)
    email = models.EmailField(unique=True)
    office = models.CharField(max_length=100, default='Cliente')
    cell = models.CharField(max_length=15)
    cep = models.CharField(max_length=9)
    address = models.CharField(max_length=255)
    access_level = models.CharField(max_length=50, default='admin')
    district = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    complement = models.CharField(max_length=100, blank=True)
    rg = models.CharField(max_length=15)
    cpf = models.CharField(max_length=14)
    password = models.CharField(max_length=128, default='1')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_groups',
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to.'
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_user_permissions',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.'
    )


    @classmethod
    def get_all_employees(cls):
        return cls.objects.all()


    @classmethod
    def search_by_username(cls, username):
        return cls.objects.filter(username__icontains=username)
    
    
    def save(self, *args, **kwargs):
        self.set_password(self.password)
        super().save(*args, **kwargs)