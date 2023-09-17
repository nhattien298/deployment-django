from django import forms
from django.contrib.auth.models import User
from basic_app.models import UserProfileInfo

class UserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
    
class UserProfileInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfileInfo
        fields =('portfolio_site', 'profile_pic')