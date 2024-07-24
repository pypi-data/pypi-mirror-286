from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import (
    AttributeMapping,
    Sensor,
    SensorType,
    Transducer,
    TransducerType,
    UserProfile,
)


class UserProfileInline(admin.StackedInline):
    """
    Class representing an inline user profile.

    Attributes
    ----------
    model : model
        The model related to the user profile.
    can_delete : bool
        Indicates whether the user profile can be deleted or not.
    verbose_name_plural : str
        The human-readable plural name for the user profile.
    fk_name : str
        The name of the foreign key that relates the user profile to the user.
    """

    model = UserProfile
    can_delete = False
    verbose_name_plural = "UserProfile"
    fk_name = "user"


class SensUserAdmin(UserAdmin):
    """
    Class representing Sens user administration.

    Attributes
    ----------
    inlines : tuple
        A tuple of inline classes associated with user administration.
    list_select_related : str
        Related fields to be selected when retrieving objects.
    list_display : list
        List of fields to display in the user administration list view.

    Methods
    -------
    get_web_config(instance)
        Gets the web configuration of the provided instance.
    get_inline_instances(request, obj=None)
        Gets inline instances for user administration.
    """

    inlines = (UserProfileInline,)
    list_select_related = ("userprofile",)
    list_display = list(UserAdmin.list_display)
    list_display.insert(1, "get_web_config")
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "password1", "password2"),
            },
        ),
    )

    def get_web_config(self, instance):
        """
        Gets the web configuration of the provided instance.

        Parameters
        ----------
        instance : object
            The instance of the user provided.

        Returns
        -------
        str
            The first ten characters of the user profile's web configuration.
        """
        return instance.userprofile.web_config[:10]

    get_web_config.short_description = "Web config"

    def get_inline_instances(self, request, obj=None):
        """
        Gets inline instances for user administration.

        Parameters
        ----------
        request : object
            The current request.
        obj : object, optional
            The current object.

        Returns
        -------
        list
            A list of inline instances for user administration.
        """
        if not obj:
            return []
        return super().get_inline_instances(request, obj)


@admin.register(SensorType)
class SensorTypeAdmin(admin.ModelAdmin):
    fields = ("name",)


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    fields = (
        "name",
        "type",
        "device",
        "customer_id",
        "serial",
    )


@admin.register(TransducerType)
class TransducerTypeAdmin(admin.ModelAdmin):
    fields = (
        "sensor_type",
        "dash",
        "name",
        "alias" "unit",
        "safety",
        "description",
        "min_custom",
        "max_custom",
        "min_warning",
        "max_warning",
        "min_critical",
        "max_critical",
    )


@admin.register(Transducer)
class TransducerAdmin(admin.ModelAdmin):
    fields = (
        "sensor",
        "type",
        "customer_id",
        "dash",
        "name",
        "alias",
        "longitud",
        "latitud",
        "elevation",
        "unit",
        "safety",
        "tag",
        "min_custom",
        "max_custom",
        "min_warning",
        "max_warning",
        "min_critical",
        "max_critical",
    )


@admin.register(AttributeMapping)
class AttributeMappingAdmin(admin.ModelAdmin):
    fields = ("name", "type", "category", "description")


from netbox.admin import admin_site

# admin.site.unregister(User)
admin_site.site_title = "Sens platform"
admin_site.site_header = "Sens admin"
admin_site.index_title = "Sens administration"
admin.site.register(User, SensUserAdmin)
