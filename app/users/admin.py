from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import TokenProxy

from .models import *


class NNAAdmin(UserAdmin):
    # Custom admin for NNAUser model
    model = NNAUser

    list_display = ('email', 'id', 'name', 'surname', 'document', 'date_of_birth', 'home', 'status', 'is_autonomy_tutor', 'description', 'created_at')
    list_filter = ('status', 'date_of_birth', 'home', 'is_autonomy_tutor', 'created_at')
    search_fields = ('email', 'id', 'email', 'name', 'surname', 'document', 'date_of_birth', 'home', 'status', 'is_autonomy_tutor', 'description',
                     'created_at')
    ordering = ('name', 'email')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name', 'surname', 'gender', 'document', 'date_of_birth',
                       'entered_at', 'therapist', 'educators', 'home', 'status', 'development_level', 'is_autonomy_tutor', 'description')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'name', 'surname', 'gender', 'document', 'date_of_birth',
                       'entered_at', 'therapist', 'educators', 'home', 'status', 'development_level', 'is_autonomy_tutor', 'description'),
        }),
    )

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super(NNAAdmin, self).get_fieldsets(request, obj)


class StaffAdmin(UserAdmin):
    # Custom admin for StaffUser model
    model = StaffUser
    list_display = ('email', 'id', 'name', 'surname', 'is_admin')
    list_filter = ('is_admin', 'roles')
    search_fields = ('email', 'id', 'name', 'surname', 'is_admin')
    ordering = ('email', 'id')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name', 'surname', 'homes', 'roles', 'is_admin')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'name', 'surname', 'homes', 'roles', 'is_admin'),
        }),
    )

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super(StaffAdmin, self).get_fieldsets(request, obj)


class RoleAdmin(admin.ModelAdmin):
    # Custom admin for Role model
    model = Role
    list_display = ('id', 'name')
    search_fields = ('id', 'name')
    ordering = ('id',)


class HomeAdmin(admin.ModelAdmin):
    # Custom admin for Location model
    model = Home
    list_display = ('id', 'name', 'address')
    search_fields = ('id', 'name', 'address')
    ordering = ('id',)

class AvatarAdmin(admin.ModelAdmin):
    # Custom admin for Avatar model
    model = Avatar
    list_display = ('id',)
    search_fields = ('id',)
    ordering = ('id',)

admin.site.register(NNAUser, NNAAdmin)
admin.site.register(StaffUser, StaffAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Home, HomeAdmin)
admin.site.register(Avatar, AvatarAdmin)
admin.site.unregister(Group)
admin.site.unregister(TokenProxy)
admin.site.site_header = 'Sirio App Administration'
