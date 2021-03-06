from django import forms
from django.utils.translation import gettext as _

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

class LogInForm(forms.Form):
    email = forms.EmailField(label='E-mail', required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_password(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')        
        if email and password:
            qs = Subscribers.objects.filter(email=email).first()
            if qs == None:
                raise forms.ValidationError(_(" Такой эмаил уже есть "))
            elif password != qs.password:
                pass_error = _("Не верный пароль")
                raise forms.ValidationError(pass_error)
        return email


class SubscribersHiddenEmailForm(forms.ModelForm):
    city = forms.ModelChoiceField(label="город", queryset=City.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    speciality = forms.ModelChoiceField(label="специальность", queryset=Speciality.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.HiddenInput())
    is_active = forms.BooleanField(label='Рассылка?', required=False, widget=forms.CheckboxInput())

    class Meta:
        model = Subscribers
        fields = ('email', 'city', 'speciality', 'password', 'is_active')

class ContactForm(forms.Form):
    email = forms.EmailField(label='E-mail', required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    city = forms.CharField(label="город", required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    speciality = forms.CharField(label="специальность", required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

