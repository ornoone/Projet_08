from django.shortcuts import render, reverse, redirect
from django.views.generic.edit import FormView
from django.views.generic import TemplateView, DetailView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .admin import UserCreationForm
from .models import Product
from .forms import ContactForm, SearchForm


# context_processors functions
def navbar_search_form(request):
    search_form = SearchForm()
    return {'search_form': search_form}


# Create your views here.
class IndexView(FormView):
    form_class = SearchForm
    template_name = 'Nutella/index.html'


class LegalView(TemplateView):
    template_name = 'Nutella/legals.html'


class ContactView(FormView):
    template_name = 'Nutella/contact.html'
    form_class = ContactForm
    success_url = 'Nutella/thanks/'


def product_view(request, product_id):
    template_name = 'Nutella/product.html'
    product = Product.objects.get(pk=product_id)
    return render(request, template_name, {'product': product})


def results(request):
    template_name = 'Nutella/results.html'
    if request.method == 'POST':
        form = SearchForm(data=request.POST)
        if form.is_valid():
            search_terms = form.cleaned_data.get('search')
            result = Product.objects.filter(category__name__icontains=search_terms)
            return render(request, template_name, {'result': result, 'search_terms': search_terms})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        print(form)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Bienvenue {username}!")
                return redirect(reverse('Nutella:index',))
    else:
        form = AuthenticationForm()
        return render(request, 'Nutella/login.html', {'form': form})


def register(request):
    template_name = 'Nutella/register.html'
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            name = form.cleaned_data.get('name')
            messages.success(request, f"Bienvenue {name}!")
            login(request, user)
            return redirect('Nutella:index',)
        else:
            for elt in form.errors.as_data():
                messages.info(request, f"{elt}: {form.errors.as_data()[elt]}")
            return redirect('Nutella:register',)
    else:
        form = UserCreationForm()
        return render(request, template_name, {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, f"Vous avez été déconnecté!")
    return redirect(reverse('Nutella:index',))


class AccountView(LoginRequiredMixin, TemplateView):
    redirect_field_name = "/account/"
    login_url = '/login/'
    template_name = 'Nutella/account.html'


def saved_food_view(request):
    template_name = 'Nutella/saved_food.html'
    return render(request, template_name)
