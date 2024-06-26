from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauths.models import User


class UserRegisterForm(UserCreationForm):
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class': '', 'id': "", 'placeholder': 'Full Name'}),
                                max_length=100, required=True)
    username = forms.CharField(widget=forms.TextInput(attrs={'class': '', 'id': "", 'placeholder': 'Username'}),
                               max_length=100, required=True)
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': '', 'id': "", 'placeholder': 'Email Address'}),
                             required=True)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'id': "", 'placeholder': 'Password'}), required=True)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'id': "", 'placeholder': 'Confirm Password'}), required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'with-border'

    class Meta:
        model = User
        fields = ['full_name', 'username', 'gender', 'phone', 'email', 'password1', 'password2']
