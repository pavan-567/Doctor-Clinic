from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class UserForm(UserCreationForm) :
    gender = forms.ChoiceField(choices= (
        ('male', 'male'),
        ('female', 'female'),
        ('other', 'other')
    ))
    class Meta : 
        model = User  
        fields = ('username', 'email', 'first_name', 'last_name', 'gender', 'password1', 'password2' )

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None