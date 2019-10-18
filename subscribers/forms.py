from django import forms

from subscribers.models import Subscribers
from scraping.models import Speciality, City

class SubscribersModelForm(forms.ModelForm):
    email = forms.EmailField(label='E-mail', required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    city = forms.ModelChoiceField(label="город", queryset=City.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    speciality = forms.ModelChoiceField(label="специальность", queryset=Speciality.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Subscribers
        fields = ('email', 'city', 'speciality', 'password')
        exclude = ('is_active',)