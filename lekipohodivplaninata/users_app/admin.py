from django.contrib import admin
from django.contrib.auth import admin as auth_admin, get_user_model
from django.utils.translation import gettext_lazy as _

from lekipohodivplaninata.users_app.models import ProfileBaseInformation

UserModel = get_user_model()


@admin.register(UserModel)
class UserAppAdmin(auth_admin.UserAdmin):
    change_user_password_template = None
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            _("Permissions"),
            {
                "fields": (
                    # "is_active",
                    # "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    # form = UserChangeForm
    # add_form = UserCreationForm
    # change_password_form = AdminPasswordChangeForm
    list_display = ("email", "is_staff")
    list_filter = ("is_staff", "is_superuser",)
    search_fields = ("email",)
    ordering = ("email",)

    # filter_horizontal = (
    #     "groups",
    #     "user_permissions",
    # )


@admin.register(ProfileBaseInformation)
class UserProfileAdmin(admin.ModelAdmin):
    pass
