from django import forms

from scraping.models import Speciality, City

class FindVacancyForm(forms.Form):
    city = forms.ModelChoiceField(label="город", queryset=City.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    speciality = forms.ModelChoiceField(label="специальность", queryset=Speciality.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))