from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import NNA, Therapist, Location


class NNAAdmin(UserAdmin):
    # Custom admin for NNA model
    model = NNA
    list_display = ('id', 'email', 'name', 'surname', 'location', 'date_of_birth', 'mentor', 'status')
    list_filter = ("status",)

    # Fieldsets for admin page
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name', 'surname', 'location', 'date_of_birth', 'mentor', 'status')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'name', 'surname', 'location', 'date_of_birth', 'mentor', 'status'),
        }),
    )
    search_fields = ('id', 'email', 'name', 'surname')
    ordering = ('id',)


class TherapistAdmin(UserAdmin):
    # Custom admin for Therapist model
    model = Therapist
    list_display = ('id', 'email', 'name', 'surname')
    list_filter = ()

    # Fieldsets for admin page
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name', 'surname')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'name', 'surname'),
        }),
    )
    search_fields = ('id', 'email', 'name', 'surname')
    ordering = ('id',)


admin.site.register(NNA, NNAAdmin)
admin.site.register(Therapist, TherapistAdmin)
admin.site.register(Location)
