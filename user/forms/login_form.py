from django import forms

class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_placeholder(self.fields['username'], 'Type your username')
        self.add_placeholder(self.fields['password'], 'Type your password')

    def add_placeholder(self, field, placeholder_text):
        field.widget.attrs['placeholder'] = placeholder_text

    username = forms.CharField()
    password = forms.CharField(
        widget=forms.PasswordInput()
    )