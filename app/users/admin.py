"""from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Home, CustomUser

class HomeAdmin(admin.ModelAdmin):
    # Custom admin for Location model
    model = Home
    list_display = ('id', 'name', 'address')
    search_fields = ('id', 'name', 'address')
    ordering = ('id',)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Home, HomeAdmin)
admin.site.site_header = 'Sirio App Administration'
"""