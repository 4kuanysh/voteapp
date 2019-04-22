from django import forms
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    
    username.widget.attrs.update({'class':"form-control" ,'placeholder':"you@example.com"})
    password.widget.attrs.update({'class':"form-control", 'placeholder':"Password"})
    
    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('This user does not exist')
            if not user.check_password(password):
                raise forms.ValidationError('Incorrect password')
            if not user.is_active:
                raise froms.ValidationError('This user is not active')
        return super(UserLoginForm, self).clean(*args, **kwargs)    
        
class UserRegisterForm(forms.ModelForm):
    
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)
    password.widget.attrs.update({'class':"form-control", 'placeholder':"Password"})
    password_confirm.widget.attrs.update({'class':"form-control", 'placeholder':"Password confirm"})
    
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
        ]

        widgets = {
            'username': forms.TextInput(attrs={'class':"form-control", 'placeholder': "Your login"}) ,
            'email': forms.TextInput(attrs={'class':"form-control", 'placeholder':"you@example.com"}),
        }

    def clean(self):
        cleaned_data = super(UserRegisterForm, self).clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        print(password, password_confirm)

        if not password or password_confirm != password:
            raise forms.ValidationError("Passwords must match")
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError("This email is already being used")
        return email
    
        