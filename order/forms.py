from django import forms

class CreditCardForm(forms.Form):
    card_number = forms.CharField(label='Número do Cartão', max_length=19)
    expiration_date = forms.DateField(label='Data de Expiração', widget=forms.SelectDateWidget)
    cvv = forms.CharField(label='CVV', max_length=3)

