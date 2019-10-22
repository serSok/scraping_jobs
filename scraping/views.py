
from django.shortcuts import render
from django.http import Http404
import datetime

from scraping.models import *
from scraping.forms import FindVacancyForm


def index(request):
    form = FindVacancyForm
    return render(request, 'scraping/home.html', {'form': form})


def vacancy_list(request):
    today = datetime.date.today()
    form = FindVacancyForm

    if request.GET:
        try:
            city_id = int(request.GET.get('city'))
            speciality_id = int(request.GET.get('speciality'))
        except ValueError:
            raise Http404('Page not found')
        context = {}
        context['form'] = form
        qs = Vacancy.objects.filter(city=city_id, speciality=speciality_id) #, timestamp=today
        if qs:
            context['jobs'] = qs
            context['city'] = qs[0].city.name
            context['speciality'] = qs[0].speciality.name
            return render(request, 'scraping/list.html', context)


    return render(request, 'scraping/list.html', {'form': form})

