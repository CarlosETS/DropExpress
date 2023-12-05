import re
from xml.dom import ValidationErr
from django import forms
from .models import CustomProduct, ProductType

class CustomProductForm(forms.ModelForm):
    class Meta:
        model = CustomProduct
        fields = '__all__'

    widgets = {
        'name': forms.TextInput(attrs={}),
        'product_type': forms.Select(choices=[(tag.name, tag.value) for tag in ProductType]),
        'description': forms.TextInput(attrs={}),
        'price': forms.NumberInput(attrs={}),
        'stock': forms.NumberInput(attrs={}),
        'image': forms.ClearableFileInput(attrs={}),
    }

    def add_placeholder(self, field_name, placeholder_text, *length_restrictions):
        widget_attrs = {'placeholder': placeholder_text}

        if length_restrictions:
            widget_attrs['maxlength'] = length_restrictions[0]
            if len(length_restrictions) > 1:
                widget_attrs['minlength'] = length_restrictions[1]

        self.fields[field_name].widget.attrs.update(widget_attrs)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].label = 'Nome'
        self.fields['name'].help_text = 'Nome do produto não pode conter caracteres especiais.'
        self.fields['name'].error_messages = {
            'required': 'Por favor, preencha o campo Nome.',
            'max_length': 'O nome não pode ter mais de 255 caracteres.',
        }
        self.add_placeholder('name', 'Digite o nome do produto', 255)

        self.fields['description'].label = 'Descrição'
        self.fields['description'].error_messages = {
            'required': 'Por favor, preencha o campo Descrição.',
            'max_length': 'A descrição não pode ter mais de 255 caracteres.',
        }
        self.add_placeholder('description', 'Digite a descrição do produto', 255)

        self.fields['price'].label = 'Preço'
        self.fields['price'].help_text = 'Digite apenas numeros para o preço do produto.'
        self.fields['price'].error_messages = {
            'required': 'Por favor, preencha o campo Preço.',
        }
        self.add_placeholder('price', '20,00')

        self.fields['stock'].label = 'Estoque'
        self.fields['stock'].help_text = 'Digite apenas nuemros para a quantidade de estoque do produto.'
        self.fields['stock'].error_messages = {
            'required': 'Por favor, preencha o campo Estoque.',
        }
        self.add_placeholder('stock', '100')


    def clean_name(self):
        name = self.cleaned_data['name']

        if not re.match(r'^[a-zA-Z0-9\s]+$', name):
            raise forms.ValidationError('O nome não pode conter caracteres especiais.')

        return name
    
    
    def clean_price(self):
        price = self.cleaned_data['code']
        if not price.isdigit():
            raise ValidationErr('Por favor, insira apenas números para o preço.')
        return price
    

    def clean_stock(self):
        stock = self.cleaned_data['code']
        if not stock.isdigit():
            raise ValidationErr('Por favor, insira apenas números para a quantidade em estoque.')
        return stock


    def clean_image(self):
        image = self.cleaned_data.get('image')

        if image:
            try:
                img = Image.open(image)
                img.verify()  # Verifica se é uma imagem válida
                img.close()

                # Verifique o tamanho máximo da imagem (por exemplo, 5 MB)
                max_size = 5 * 1024 * 1024  # 5 MB em bytes
                if image.size > max_size:
                    raise forms.ValidationError('A imagem não pode ter mais de 5 MB.')

            except Exception as e:
                raise forms.ValidationError('A imagem é inválida. Certifique-se de enviar um arquivo de imagem válido.')

        return image