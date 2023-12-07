import os
from django.core.management.base import BaseCommand
from django.core.files import File
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
                    'image_path': '/path/to/images/mobile.jpg',
                },
                {
                    'name': 'Smart TV 4K',
                    'description': 'Ultra HD Smart TV with amazing visuals.',
                    'price': 999.99,
                    'stock': 30,
                    'product_type': 'TV',
                    'image_path': '/path/to/images/tv.jpg',
                },
                {
                    'name': 'Professional Camera ABC',
                    'description': 'High-performance professional camera.',
                    'price': 1499.99,
                    'stock': 20,
                    'product_type': 'CAMERA',
                    'image_path': '/path/to/images/camera.jpg',
                },
                {
                    'name': 'Laptop Pro',
                    'description': 'Powerful laptop for professionals.',
                    'price': 1299.99,
                    'stock': 25,
                    'product_type': 'LAPTOP',
                    'image_path': '/path/to/images/laptop.jpg',
                },
                {
                    'name': 'Tablet SuperTab',
                    'description': 'Sleek and efficient tablet.',
                    'price': 499.99,
                    'stock': 40,
                    'product_type': 'TABLET',
                    'image_path': '/path/to/images/tablet.jpg',
                },
                {
                    'name': 'Premium Speaker System',
                    'description': 'High-quality speaker system for immersive audio.',
                    'price': 299.99,
                    'stock': 15,
                    'product_type': 'SPEAKER',
                    'image_path': '/path/to/images/speaker.jpg',
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
                    image_path = product_data.get('image_path')
                    if image_path and os.path.exists(image_path):
                        with open(image_path, 'rb') as image_file:
                            product.image.save(os.path.basename(image_path), File(image_file))

                    product.save()
                    print(f'Product "{product.name}" created successfully with image.')
                else:
                    print(f'Form is not valid for product "{product_data["name"]}". Product not created.')
                    print(form.errors)
        else:
            print('Products can only be initialized if no products exist')
