from django.apps import apps
from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group as BaseGroup
from django.utils.translation import gettext_lazy as _

from milea_users.models import Group, MileaUserOption, Profile, User


class ProfileInline(admin.TabularInline):
    model = Profile
    extra = 0
    can_delete = False

    def has_add_permission(self, *args, **kwargs):
        return True

    def has_change_permission(self, request, obj=None):
        return True

# Diese Funktion erzeugt eine InlineAdmin-Klasse für ein option Modell
def create_milea_user_option_inline(mdl):
    class MileaUserOptionInline(admin.TabularInline):
        model = mdl
        extra = 1
        min_num = 1
        can_delete = False

        def has_change_permission(self, *args, **kwargs):
            return True

    return MileaUserOptionInline


# Remove the Default Group from the Default App and Register the Proxy
admin.site.unregister(BaseGroup)
@admin.register(Group)
class GroupAdmin(BaseGroupAdmin):
    pass


# Register New User Admin
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'last_login', 'is_active', 'is_staff')
    search_fields = ('email',)
    readonly_fields = ['last_login', 'date_joined']
    ordering = ('id',)
    inlines = [ProfileInline]

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        (_("Important dates"), {'fields': (('last_login', 'date_joined'),)}),
    )
    add_fieldsets = (
        (None, {'fields': ('email', 'password1', 'password2')}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):

    exclude = ['user',]

    fieldsets = (
        (_("Personal info"), {'fields': (('first_name', 'last_name',),)}),
    )

    # Allow user to edit own notification settings
    def has_change_permission(self, request, obj=None):
        opts = self.opts
        has_perm = request.user.has_perm("%s.%s" % (opts.app_label, "change_own_profile"))
        if obj and obj.user == request.user and has_perm:
            return True
        return super().has_change_permission(request, obj)

    def has_add_permission(self, *args, **kwargs):
        return False

    def has_delete_permission(self, *args, **kwargs):
        return False

    def get_inlines(self, request, obj):
        inlines = []
        for model in apps.get_models():
            if issubclass(model, MileaUserOption) and not model._meta.abstract:
                inlines.append(create_milea_user_option_inline(model))
        return inlines
