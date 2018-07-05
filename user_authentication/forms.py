from django import forms

from django.contrib.auth import authenticate, get_user_model, login, logout


# Collect the User model
User = get_user_model()


# Login form
class UserLoginForm(forms.Form):
    """
    Basic Login form using username and password as their field.
    """
    username = forms.CharField(
        max_length=30,
        label="Username",
        widget=forms.TextInput(attrs={'placeholder': 'Username'})
    )

    password = forms.CharField(
        label="password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )


    # verify the user credentials
    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        user = authenticate(username=username, password=password)

        if username and password:
            if not user:
                raise forms.ValidationError("This user does not exist")

            if not user.check_password(password):
                raise forms.ValidationError("Incorrect password")

            if not user.is_active:
                raise forms.ValidationError("This user is no longer active")

        return super(UserLoginForm, self).clean()



# Sign up form
class UserRegisterForm(forms.ModelForm):
    """
    Basic user registration.

    Can think of integrating email verification, but as of now, it's not being
    thought of.
    """
    username = forms.CharField(
        max_length=30,
        label='Username',
        widget=forms.TextInput(attrs={'placeholder': 'Username'})
    )

    first_name = forms.CharField(
        max_length=30,
        label='First Name',
        widget=forms.TextInput(attrs={'placeholder': 'First Name'})
    )

    last_name = forms.CharField(
        max_length=30,
        label='Last Name',
        widget=forms.TextInput(attrs={'placeholder': 'Last Name'})
    )

    email = forms.EmailField(
        max_length=255,
        label='Email address',
        widget=forms.EmailInput(attrs={'placeholder': 'Email'})
    )

    email2 = forms.EmailField(
        max_length=255,
        label='Confirm Email',
        widget=forms.EmailInput(attrs={'placeholder': 'Confirm Email'})
    )

    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )


    # Meta class to determine the order of form
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email2',
            'email',
            'password',
        ]


    # Verification for email.
    def clean_email(self):
        email = self.cleaned_data.get('email')
        email2 = self.cleaned_data.get('email2')
        if email != email2:
            raise forms.ValidationError("Emails should match.")

        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError("This email has already been taken")

        return email
