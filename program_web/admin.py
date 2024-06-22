from django.contrib import admin
from program_web.models import MyUser, Feedback, Bottle, Favourites


@admin.register(MyUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', )
@admin.register(Bottle)
class BottleAdmin(admin.ModelAdmin):
    list_display = ("name_ua", "name_eng", "kind", "country")
    list_filter = ("kind", "country")

@admin.register(Favourites)
class FavouritesAdmin(admin.ModelAdmin):
    list_display = ("user", "bottle")
    list_filter = ("user", "bottle")

@admin.register(Feedback)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'time')
    list_filter = ("name", )