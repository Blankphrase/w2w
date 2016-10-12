from django import forms

from accounts.models import User, UserProfile


EMPTY_EMAIL_ERROR = "Valid Email address is required"
UNIQUE_EMAIL_ERROR = "User with this Email address already exists"
EMPTY_PASSWORD_ERROR = "Password is required"
EMPTY_PASSWORD2_ERROR = "Password confirmation is required"
DIFFERENT_PASSWORDS_ERROR = "Your passwords do not match"
INVALID_LOGIN_ERROR = "Email address or password is invalid"


class SignUpForm(forms.ModelForm):
    
    password2 = forms.CharField(required = True, widget = forms.PasswordInput())

    class Meta:
        model = User
        fields = [ "email", "password" ]
        widgets = {
            "password": forms.PasswordInput(),
        }
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


    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit = False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):

    email = forms.EmailField(required = True, error_messages = {
        'required': EMPTY_EMAIL_ERROR}
    )
    password = forms.CharField(required = True, 
        widget = forms.PasswordInput(),
        error_messages = {'required': EMPTY_PASSWORD_ERROR}
    )


class EditProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = [ "birthday", "sex", "country" ]