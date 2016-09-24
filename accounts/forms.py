from django import forms

from accounts.models import User


EMPTY_EMAIL_ERROR = "Valid Email address is required"
UNIQUE_EMAIL_ERROR = "User with this Email address already exists"
EMPTY_PASSWORD_ERROR = "Password is required"
EMPTY_PASSWORD2_ERROR = "Password confirmation is required"
DIFFERENT_PASSWORDS_ERROR = "Your passwords do not match"


class SignUpForm(forms.ModelForm):
    
    password2 = forms.CharField(required = True)

    class Meta:
        model = User
        fields = [ "email", "password" ]

        error_messages = {
            "email": { 
                "required": EMPTY_EMAIL_ERROR, 
                "unique": UNIQUE_EMAIL_ERROR
            },
            "password": { "required": EMPTY_PASSWORD_ERROR }
        }

    def clean(self):
        super(SignUpForm, self).clean()

        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if not password2:
            raise forms.ValidationError(EMPTY_PASSWORD2_ERROR)
        if password != password2:
            raise forms.ValidationError(DIFFERENT_PASSWORDS_ERROR)

        return self.cleaned_data