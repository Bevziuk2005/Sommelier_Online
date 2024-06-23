from django.urls import reverse
from django.views import View
from .models import Bottle, Favourites
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import LoginForm, SignupForm
from .forms import SearchForm
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST

"""
                    Authorisation System
"""


class Open(View):
    def get(self, request):
        return render(request, 'program_web/open.html')

class Logout(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('program_web:search'))


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('program_web:search')
    else:
        form = LoginForm()
    return render(request, 'program_web/login.html', {'form': form})


def registration(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect(reverse('program_web:search'))
    else:
        form = SignupForm()
    return render(request, 'program_web/registration.html', {'form': form})


"""
                        Personal page for wine
"""


class White(View):
    bottles = Bottle.objects.filter(kind="біле")
    def get(self, request):
        if request.user.is_authenticated:
            favorites = Favourites.objects.filter(user=request.user)
            favorite_pk_set = set(favorite.bottle.pk for favorite in favorites)
        else:
            favorite_pk_set = set()
        dicts = {bottle.pk: (bottle.pk in favorite_pk_set) for bottle in self.bottles}
        return render(request, 'program_web/white.html', {'bottles': self.bottles, 'dicts': dicts})


class Rose(View):
    def get(self, request):
        return render(request, 'program_web/rose.html')


class Dessert(View):
    bottles = Bottle.objects.filter(kind="десертне")
    def get(self, request):
        if request.user.is_authenticated:
            favorites = Favourites.objects.filter(user=request.user)
            favorite_pk_set = set(favorite.bottle.pk for favorite in favorites)
        else:
            favorite_pk_set = set()
        dicts = {bottle.pk: (bottle.pk in favorite_pk_set) for bottle in self.bottles}
        return render(request, 'program_web/dessert.html', {'bottles': self.bottles, 'dicts': dicts})


class Sparkling(View):
    bottles = Bottle.objects.filter(kind="ігристе")
    def get(self, request):
        if request.user.is_authenticated:
            favorites = Favourites.objects.filter(user=request.user)
            favorite_pk_set = set(favorite.bottle.pk for favorite in favorites)
        else:
            favorite_pk_set = set()
        dicts = {bottle.pk: (bottle.pk in favorite_pk_set) for bottle in self.bottles}
        return render(request, 'program_web/sparkling.html', {'bottles': self.bottles, 'dicts': dicts})


class Red(View):
    bottles = Bottle.objects.filter(kind="червоне")
    def get(self, request):
        if request.user.is_authenticated:
            favorites = Favourites.objects.filter(user=request.user)
            favorite_pk_set = set(favorite.bottle.pk for favorite in favorites)
        else:
            favorite_pk_set = set()
        dicts = {bottle.pk: (bottle.pk in favorite_pk_set) for bottle in self.bottles}
        return render(request, 'program_web/red.html', {'bottles': self.bottles, 'dicts': dicts})


class Favorites(View):
    def get(self, request):
        return render(request, 'program_web/favorites.html')

"""
                        General Function
"""


def search(request):
    form = SearchForm(request.POST or None)
    results = []
    dicts = dict()

    if request.method == 'POST' and form.is_valid():
        query = form.cleaned_data['query']
        results = Bottle.objects.filter(
            Q(name_ua__icontains=query) |
            Q(name_eng__icontains=query) |
            Q(taste__icontains=query)
        )

        favorites = Favourites.objects.filter(user=request.user)
        bottles_pk = [bottle.pk for bottle in results]
        favorite_pk = [favorite.bottle.pk for favorite in favorites]

        for i in bottles_pk:
            if i in favorite_pk:
                dicts[i] = True

    return render(request, 'program_web/search.html', {'form': form, 'results': results, 'dicts': dicts})


from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST
from .models import Bottle, Favourites


@require_POST
def favorite(request, pk, site):
    bottle = get_object_or_404(Bottle, pk=pk)
    if request.user.is_authenticated:
        user_id = request.user.id
    else:
        user_id = 0

    Favourites.objects.create(user_id=user_id, bottle=bottle)

    # Ensure the site parameter is cleaned up
    urls = site.strip('/').split('/')

    # Handle redirection based on the cleaned URLs
    if len(urls) == 1 and urls[0]:
        return redirect('program_web:' + urls[0])
    elif len(urls) == 2:
        return redirect('program_web:search')

    # Default fallback if the site parameter is not as expected
    return redirect('program_web:index')  # Adjust as necessary


"""
@require_POST
def favorite(request, pk, site):
    bottle = get_object_or_404(Bottle, pk=pk)
    if request.user.is_authenticated:
        user_id = request.user.id
    else:
        user_id = 0
    Favourites.objects.create(user_id=user_id, bottle=bottle)
    urls = site.split('/')
    url = [url for url in urls if url != '']
    if len(url) == 2:
        return redirect('program_web:search')
    return redirect('program_web:' + urls[-1])
"""
def user_favorites(request):
    favorites = Favourites.objects.filter(user=request.user)
    bottles = [fav.bottle for fav in favorites]
    return render(request, 'program_web/favorites.html', {'bottles': bottles})


def remove_favorite(request, pk):
    bottle = Bottle.objects.get(pk=pk)
    favorite = Favourites.objects.filter(user=request.user, bottle=bottle)
    if favorite.exists():
        favorite.delete()
    return redirect('program_web:favorites')

