from django.shortcuts import render
from django.db import IntegrityError
from django.http import Http404

from scraping.utils import *
from scraping.models import *
from scraping.forms import FindVacancyForm

# def index(request):
#     form = FindVacancyForm
#     return render(request, 'scraping/list.html', {'form': form})


def list_v(request):
    today = datetime.date.today()
    city = City.objects.get(name='Киев')
    speciality = Speciality.objects.get(name='Python')
    qs = Vacancy.objects.filter(city=city.id, speciality=speciality.id, timestamp=today)
    if qs:
        return render(request, 'scraping/list.html', {'jobs': qs})
    return render(request, 'scraping/list.html')


# def vacancy_list(request):
#     today = datetime.date.today()
#     form = FindVacancyForm

#     if request.GET:
#         try:
#             city_id = int(request.GET.get('city'))
#             speciality_id = int(request.GET.get('speciality'))
#         except ValueError:
#             raise Http404('Page not found')
#         context = {}
#         context['form'] = form
#         qs = Vacancy.objects.filter(city=city_id, speciality=speciality_id, timestamp=today)
#         if qs:
#             context['jobs'] = qs
#             return render(request, 'scraping/list.html', context)


#     return render(request, 'scraping/list.html', {'form': form})




def home(request):

    city = City.objects.get(name='Киев')
    speciality = Speciality.objects.get(name='Python')
    url_qs = Url.objects.filter(city = city, speciality = speciality)
    site = Site.objects.all()

    url_w = url_qs.get(site=site.get(name='Work.ua')).url_address
    url_dj = url_qs.get(site=site.get(name='djinni.co')).url_address
    url_r = url_qs.get(site=site.get(name='Rabota.ua')).url_address
    url_dou = url_qs.get(site=site.get(name='Dou.ua')).url_address

    jobs = []
    jobs.extend(work(url_w))
    jobs.extend(djinni(url_dj))
    jobs.extend(rabota(url_r))
    jobs.extend(dou(url_dou))

    # v = Vacancy.objects.filter(city=city.id, speciality=speciality.id).values('url')
    # url_list = [i['url'] for i in v]
    for job in jobs:
        # if job['href'] not in url_list:
        vacancy = Vacancy(city=city, speciality=speciality, url = job['href'], 
                        title = job['title'], description = job['descript'], company = job['company'])
        try:
            vacancy.save()
        except IntegrityError:
            pass
            

    return render(request, 'scraping/list.html', {'jobs': jobs})
