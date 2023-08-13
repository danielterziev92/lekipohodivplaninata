from django.contrib import admin
from django.contrib.auth import admin as auth_admin, get_user_model
from django.forms import inlineformset_factory
from django.utils.translation import gettext_lazy as _

from lekipohodivplaninata.users_app.models import BaseProfile, GuideProfile

UserModel = get_user_model()

BaseProfileFormSet = inlineformset_factory(
    UserModel, BaseProfile,
    fields=('first_name', 'last_name', 'phone_number')
)


class BaseProfileInline(admin.StackedInline):
    model = BaseProfile
    formset = BaseProfileFormSet
    extra = 1

    fieldsets = (
        (
            _('Данни за потребителя'),
            {
                'fields': ('first_name', 'last_name', 'phone_number'),
            }),
    )


@admin.register(UserModel)
class UserAppAdmin(auth_admin.UserAdmin):
    inlines = (BaseProfileInline,)
    change_user_password_template = None
    fieldsets = (
        (None, {'fields': ('email',)}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                ),
            },
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ('wide',),
                "fields": ('email', 'password1', 'password2'),
            },
        ),
    )
    list_display = ('email', 'get_first_name', 'get_last_name', 'get_phone_number', 'is_staff', 'last_login')
    list_filter = ('is_staff', 'is_superuser',)
    search_fields = ('email',)
    ordering = ('email',)

    def get_first_name(self, obj):
        base_profile = obj.baseprofile
        return base_profile.first_name if base_profile else ""

    def get_last_name(self, obj):
        base_profile = obj.baseprofile
        return base_profile.last_name if base_profile else ""

    def get_phone_number(self, obj):
        base_profile = obj.baseprofile
        return base_profile.phone_number if base_profile else ""

    get_first_name.short_description = 'Име'
    get_last_name.short_description = 'Фамилия'
    get_phone_number.short_description = 'Телефон'


# @admin.register(BaseProfile)
# class UserProfileAdmin(admin.ModelAdmin):
#     fieldsets = (
#         (None, {'fields': ('user_id',)}),
#         (_('Лични данни'), {
#             'fields': ('first_name', 'last_name',)
#         })
#     )


@admin.register(GuideProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('avatar_picture', 'user_id', 'full_name', 'date_of_birth',)
    list_display_links = ('user_id',)

    # fields = [field.name for field in GuideProfile._meta.get_fields() if field.name != 'trekswithguidesandusers']
    # print(fields)

    fieldsets = (
        (None, {'fields': ('user_id', 'profile_id',)}),
        (_('За мен'), {
            'fields': ('date_of_birth', 'description',)
        }),
        (_('Снимки'), {
            'fields': ('avatar', 'certificate',),
        }),
    )

    def avatar_picture(self, obj: GuideProfile):
        return obj.avatar_picture

    def full_name(self, obj: GuideProfile):
        return obj.get_full_name

    avatar_picture.short_description = 'Снимка'
    avatar_picture.allow_tags = True
    full_name.short_description = 'Име и фамилия'
    full_name.allow_tags = True
