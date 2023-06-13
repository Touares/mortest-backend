# Register your models here.
from django import forms
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class MyUserAdmin(UserAdmin):
    model = CustomUser

class UserCreationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username',)

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

# class CustomUserChangeForm(UserChangeForm):
#     """A form for updating users. Includes all the fields on
#     the user, but replaces the password field with admin's
#     password hash display field.
#     """

#     def __init__(self, *args, **kargs):
#         super(CustomUserChangeForm, self).__init__(*args, **kargs)
#         del self.fields['username']

#     class Meta:
#         model = CustomUser
#         fields = ('username',)

class CustomUserAdmin(UserAdmin):
    # The forms to add and change user instances
    add_form = UserCreationForm
    # form = CustomUserChangeForm
    list_display = ("username",)
    ordering = ("username",)

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'first_name', 
        'last_name', 'user_permissions', 'is_staff', "is_superuser")}),
        )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password', 'first_name', 'last_name', 'user_permissions', 'is_superuser', 'is_staff', 'is_active')}
            ),
        )

    filter_horizontal = ()
# admin.site.unregister(CustomUser)
admin.site.register(CustomUser, CustomUserAdmin)
