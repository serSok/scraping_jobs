from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import FormView, CreateView
from django.urls import reverse_lazy
from django.contrib import messages

from .forms import SubscribersModelForm, LogInForm, SubscribersHiddenEmailForm
from .models import Subscribers

class SubscribersCreate(CreateView):
    model = Subscribers
    form_class = SubscribersModelForm
    template_name = 'subscribers/create.html'
    success_url = reverse_lazy('create')

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            messages.success(request, "Успешно сохранили")
            return self.form_valid(form)
        else:
            messages.error(request, "Ошибка заполнения")
            return self.form_invalid(form)

def login_subscriber(request):
    if request.method == 'GET':
        form = LogInForm
        return render(request, 'subscribers/login.html', {'form': form})
    elif request.method == 'POST':
        form = LogInForm(request.POST or None)
        if form.is_valid():
            data = form.cleaned_data
            request.session['email'] = data['email']
            return redirect('update')
        return render(request, 'subscribers/login.html', {'form': form})
        
def update_subscriber(request):
    if request.method == 'GET' and request.session.get('email', False):
        email = request.session.get('email')
        qs = Subscribers.objects.filter(email=email).first()
        form = SubscribersHiddenEmailForm(initial={'email': qs.email , 'city': qs.city, 'speciality': qs.speciality, 'password': qs.password, 'is_active': qs.is_active})
        return render(request, 'subscribers/update.html', {'form': form})
    elif request.method == 'POST':
        email = request.session.get('email')
        user = get_object_or_404(Subscribers, email=email)
        form = SubscribersHiddenEmailForm(request.POST or None, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Успешно сохранили")
            del request.session['email']
            return redirect('list')
        messages.error(request, "Ошибка заполнения")
        return render(request, 'subscribers/update.html', {'form': form})
    else:
        return redirect('login')



