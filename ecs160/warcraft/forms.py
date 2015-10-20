from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class MyRegistrationForm(UserCreationForm):
    email = forms.EmailField(required = True)
    avatar = forms.ImageField(required = True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'avatar', 'password1', 'password2')
    
    def save(self, commit = True):
        user = super(UserCreationForm, self).save(commit = False)
        user.email = self.cleaned_data['email']
        user.avatar = self.cleaned_data['avatar']
        
        if commit:
            user.save()
            
        return user