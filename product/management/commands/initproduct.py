import os
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from product.forms import CustomProductForm
from product.models import CustomProduct

class Command(BaseCommand):
    def handle(self, *args, **options):
        if CustomProduct.objects.count() == 0:
            print('Creating products with images...')

            products_data = [
                {
                    'name': 'Mobile Phone XYZ',
                    'description': 'Feature-rich mobile phone.',
                    'price': 699.99,
                    'stock': 50,
                    'product_type': 'MOBILE',
                    'image': 'product_image/Phone-1.jpg',
                },
                {
                    'name': 'Mobile Phone XZ',
                    'description': 'Feature-rich mobile phone.',
                    'price': 899.99,
                    'stock': 50,
                    'product_type': 'MOBILE',
                    'image': 'product_image/Phone-2.jpg',
                },
                {
                    'name': 'Smart TV 4K LG',
                    'description': 'Ultra HD Smart TV with amazing visuals.',
                    'price': 899.99,
                    'stock': 30,
                    'product_type': 'TV',
                    'image': 'product_image/Tv-1.jpg',
                },
                {
                    'name': 'Smart TV 4K',
                    'description': 'Ultra HD Smart TV with amazing visuals.',
                    'price': 999.99,
                    'stock': 30,
                    'product_type': 'TV',
                    'image': 'product_image/Tv-2.jpg',
                },
                {
                    'name': 'Professional Camera ABC',
                    'description': 'High-performance professional camera.',
                    'price': 1499.99,
                    'stock': 20,
                    'product_type': 'CAMERA',
                    'image': 'product_image/Camera-1.jpg',
                },
                {
                    'name': 'Professional Camera Polishop',
                    'description': 'High-performance professional camera.',
                    'price': 1299.99,
                    'stock': 20,
                    'product_type': 'CAMERA',
                    'image': 'product_image/Camera-2.jpg',
                },
                {
                    'name': 'Laptop Pro',
                    'description': 'Powerful laptop for professionals.',
                    'price': 1299.99,
                    'stock': 25,
                    'product_type': 'LAPTOP',
                    'image': 'product_image/Laptop-1.jpg',
                },
                {
                    'name': 'Laptop Pro Sansung',
                    'description': 'Powerful laptop for professionals.',
                    'price': 1299.99,
                    'stock': 25,
                    'product_type': 'LAPTOP',
                    'image': 'product_image/Laptop-2.jpg',
                },
                {
                    'name': 'Tablet SuperTab',
                    'description': 'Sleek and efficient tablet.',
                    'price': 499.99,
                    'stock': 40,
                    'product_type': 'TABLET',
                    'image': 'product_image/Tablet-1.jpg',
                },
                {
                    'name': 'Tablet SuperTab LG',
                    'description': 'Sleek and efficient tablet.',
                    'price': 499.99,
                    'stock': 40,
                    'product_type': 'TABLET',
                    'image': 'product_image/Tablet-2.jpg',
                },
                {
                    'name': 'Premium Speaker System',
                    'description': 'High-quality speaker system for immersive audio.',
                    'price': 299.99,
                    'stock': 15,
                    'product_type': 'SPEAKER',
                    'image': 'product_image/Speaker-1.jpg',
                },
                {
                    'name': 'Premium Speaker System JBL',
                    'description': 'High-quality speaker system for immersive audio.',
                    'price': 299.99,
                    'stock': 15,
                    'product_type': 'SPEAKER',
                    'image': 'product_image/Speaker-2.jpg',
                },
            ]

        for product_data in products_data:
            form_data = {
                'name': product_data['name'],
                'description': product_data['description'],
                'price': product_data['price'],
                'stock': product_data['stock'],
                'product_type': product_data['product_type'],
            }

            form = CustomProductForm(form_data)

            if form.is_valid():
                product = form.save(commit=False)

                # Attach image
                image = product_data.get('image')
                if image:
                    product.image.save(f"{product_data['name']}.jpg", ContentFile(image), save=True)
                    print(f'Product "{product.name}" created successfully with image.')
                else:
                    print(f'Form is not valid for product "{product_data["name"]}". Product not created.')
                    print(form.errors)
            else:
                print(f'Form is not valid for product "{product_data["name"]}". Product not created.')
                print(form.errors)
        print('Products creation completed.')