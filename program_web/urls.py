from django.urls import path, include
from .views import Open,  Logout, White, Rose, Dessert, Sparkling, Red, registration, user_login, search, favorite, user_favorites, remove_favorite

app_name = 'program_web'
urlpatterns = [
    path('', search, name='search'),

    path('open', Open.as_view(), name='open'),
    path('login',user_login,name='login'),
    path('logout', Logout.as_view(), name='logout'),
    path('registration',registration,name='registration'),

    path('white', White.as_view(), name='white'),
    path('rose', Rose.as_view(), name='rose'),
    path('dessert', Dessert.as_view(), name='dessert'),
    path('sparkling', Sparkling.as_view(), name='sparkling'),
    path('red', Red.as_view(), name='red'),

    path('favorite/<int:pk>/<path:site>/', favorite, name='favorite'),
    path('favorites', user_favorites, name='favorites'),
    path('remove_favorite/<int:pk>/', remove_favorite, name='remove_favorite')
]
