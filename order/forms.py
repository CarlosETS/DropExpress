from django import forms

class CreditCardForm(forms.Form):
    name= forms.CharField(label='Nome como esta no catão', max_length=255, min_length=12)
    card_number = forms.CharField(label='Número do Cartão', max_length=19)
    expiration_date = forms.DateField(label='Data de Expiração', widget=forms.SelectDateWidget)
    cvv = forms.CharField(label='CVV', max_length=3)

