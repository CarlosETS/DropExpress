from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=128)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    cell = models.CharField(max_length=15)
    cep = models.CharField(max_length=10)
    address = models.CharField(max_length=255)
    complement = models.CharField(max_length=255)
    district = models.CharField(max_length=50)
    city = models.CharField(max_length=50)


    def __str__(self):
        return self.username
   
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


    def save(self, *args, **kwargs):
        # Certifique-se de não chamar set_password se não houver password definido no modelo.
        if self.password:
            self.set_password(self.password)
        super().save(*args, **kwargs)