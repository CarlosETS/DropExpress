from django import forms

class CreditCardForm(forms.Form):
    card_number = forms.CharField(label='Número do Cartão', max_length=16)
    expiration_date = forms.DateField(label='Data de Expiração', widget=forms.SelectDateWidget)
    cvv = forms.CharField(label='CVV', max_length=4)
    # Outros campos necessários podem ser adicionados conforme necessário
