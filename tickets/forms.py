from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.Form):
    # Formulário para registro de uma conta nova
    firstname = forms.CharField(label="Primeiro Nome: ")
    lastname = forms.CharField(label="Ultimo Nome: ")
    email = forms.EmailField(label="Endereço de Email: ")
    password = forms.CharField(
        label="Password: ",
        widget=forms.PasswordInput(render_value=True),
        min_length=6,
        max_length=14
    )
    password_conf = forms.CharField(
        label="Confirmação da Password: ",
        widget=forms.PasswordInput
    )

    def clean(self):
        # Validação do formulário
        super(RegisterForm, self).clean()

        # Extração de dados do utilizador
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        password_conf = self.cleaned_data.get('password_conf')

        # Confirmar que a Password é igual a password_conf
        if password != password_conf:
            self._errors['password_conf'] = self.error_class([
                "Confirmação Errada!"
            ])

        # Confirmar que o email não se encontra em uso
        if User.objects.filter(username=email).exists():
            self._errors['email'] = self.error_class(['Email já se encontra em uso'])

        # Fazer return de erros encontrados
        return self.cleaned_data


class LoginForm(forms.Form):
    # Formulário para Login
    email = forms.EmailField(label="Endereço de Email: ")
    password = forms.CharField(
        label="Password: ",
        widget=forms.PasswordInput
    )
