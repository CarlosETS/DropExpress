from typing import Any
from django import forms
from .models import CustomUser
from django.core.exceptions import ValidationError


class CustomUserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        print(*args)
        super().__init__(*args, **kwargs)
        self.add_placeholder('code', 'Digite o código', '10', '10')
        self.add_placeholder('username', 'Digite o nome')
        self.add_placeholder('email', 'email@email.com')
        self.add_placeholder('office', 'Digite o cargo')
        self.add_placeholder('cell', '(44) 99999-9999', '15', '14')
        self.add_placeholder('cep', '85000-000', '9', '9')
        self.add_placeholder('address', 'Digite o endereço')
        self.add_placeholder('access_level', 'Digite o nível de acesso')
        self.add_placeholder('district', 'Digite o bairro')
        self.add_placeholder('city', 'Digite a cidade')
        self.add_placeholder('complement', 'Digite o complemento', '255')
        self.add_placeholder('rg', '44.555.666-77', '15', '15')
        self.add_placeholder('cpf', '888.999.111-99', '14', '14')
        self.add_placeholder('password', 'Digite a senha', '128', '8')


    def add_placeholder(self, field_name, placeholder_text, *length_restrictions):
        widget_attrs = {'placeholder': placeholder_text}

        if length_restrictions:
            widget_attrs['maxlength'] = length_restrictions[0]
            if len(length_restrictions) > 1:
                widget_attrs['minlength'] = length_restrictions[1]

        self.fields[field_name].widget.attrs.update(widget_attrs)

    code = forms.CharField(
        label='Código',
        help_text=(
            'O código não pode ter mais de 10 caracteres. '
            'Por favor, insira apenas números.'
        ),
        error_messages={
            'required': 'Por favor, preencha o campo Código.',
            'max_length': 'O código não pode ter mais de 10 caracteres.',
            'invalid': 'Por favor, insira apenas números.',
        },
    )

    username = forms.CharField(
        label='Nome',
        error_messages={
            'required': 'Por favor, preencha o campo Nome.',
            'min_length': 'O nome deve ter pelo menos 3 caracteres.',
            'max_length': 'O nome não pode ter mais de 50 caracteres.',
        },
    )

    email = forms.EmailField(
        label='Email',
        help_text='O Email deve ser válido ex@gmail.com',
        error_messages={
            'required': 'Por favor, preencha o campo E-mail.',
            'invalid': 'Por favor, insira um endereço de e-mail válido.',
        },
    )

    office = forms.CharField(
        label='Cargo',
        error_messages={
            'required': 'Por favor, preencha o campo Cargo.',
            'max_length': 'O cargo não pode ter mais de 50 caracteres.',
        },
    )

    cell = forms.CharField(
        label='Celular',
        error_messages={
            'required': 'Por favor, preencha o campo Celular.',
            'max_length': 'O número do celular não pode ter mais de 15 caracteres.',
        },
    )

    cep = forms.CharField(
        label='CEP',
        error_messages={
            'required': 'Por favor, preencha o campo CEP.',
            'max_length': 'O CEP deve ter 8 caracteres.',
        },
    )

    address = forms.CharField(
        label='Endereço',
        error_messages={
            'required': 'Por favor, preencha o campo Endereço.',
            'max_length': 'O endereço não pode ter mais de 100 caracteres.',
        },
    )

    access_level = forms.CharField(
        label='Nível de Acesso',
        error_messages={
            'required': 'Por favor, selecione um Nível de Acesso.',
        },
        widget=forms.TextInput(attrs={'placeholder': 'Digite o nível de acesso', 'maxlength': '50'}),
    )

    district = forms.CharField(
        label='Bairro',
        error_messages={
            'required': 'Por favor, preencha o campo Bairro.',
            'max_length': 'O bairro não pode ter mais de 50 caracteres.',
        },
    )

    city = forms.CharField(
        label='Cidade',
        error_messages={
            'required': 'Por favor, preencha o campo Cidade.',
            'max_length': 'A cidade não pode ter mais de 50 caracteres.',
        },
    )

    complement = forms.CharField(
        label='Complemento',
        error_messages={
            'required': 'Por favor, preencha o campo Complemento.',
            'max_length': 'O complemento não pode ter mais de 50 caracteres.',
        },
    )

    rg = forms.CharField(
        label='RG',
        error_messages={
            'required': 'Por favor, preencha o campo RG.',
            'max_length': 'O RG não pode ter mais de 15 caracteres.',
        },
    )

    cpf = forms.CharField(
        label='CPF',
        error_messages={
            'required': 'Por favor, preencha o campo CPF.',
            'max_length': 'O CPF deve ter 11 caracteres.',
        },
    )

    password = forms.CharField(
        label='Senha',
        help_text=(
            'A senha deve ter pelo menos 8 caracteres '
            'e conter letras maiúsculas, minúsculas, números e caracteres especiais.'
        ),
        error_messages={
            'required': 'Por favor, preencha o campo Senha.',
            'min_length': 'A senha deve ter pelo menos 8 caracteres.',
        },
    )


    class Meta:
        model = CustomUser
        fields = (
            'code', 'username', 'email',
            'office', 'cell', 'cep',
            'address', 'access_level',
            'district', 'city', 'complement',
            'rg', 'cpf', 'password'
        )


    def clean_code(self):
        code = self.cleaned_data['code']
        if not code.isdigit():
            raise ValidationError('Por favor, insira apenas números para o código.')
        return code


    def clean_email(self):
        email = self.cleaned_data['email']
        return email
    

class LoginForm(forms.Form):
    username = forms.CharField(label='Usuário', max_length=100, widget=forms.TextInput(attrs={'placeholder': ("Usuário")}))
    password = forms.CharField(label='Senha', widget=forms.PasswordInput(attrs={'placeholder': ("Senha")}))


    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['class'] = 'form-control'


class EditUserForm(CustomUserForm):
    password = forms.CharField(
        label='Nova Senha',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        required=False,
        help_text=(
            "Nova senha"
        ),
    )
    code = forms.CharField(disabled=True)


    class Meta:
        model = CustomUser
        fields = (
            'code', 'username', 'email', 
            'office', 'cell', 'cep', 
            'address', 'access_level', 
            'district', 'city', 'complement', 
            'rg', 'cpf', 'password'
        )


class EmployeeListForm(forms.Form):
    q = forms.CharField(label='', required=False, widget=forms.TextInput(attrs={'placeholder': 'Pesquisar funcionários...'}))