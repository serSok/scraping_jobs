from django.shortcuts import render
from django.views.generic.edit import FormView, CreateView
from django.urls import reverse_lazy
from django.contrib import messages

from .forms import SubscribersModelForm
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


