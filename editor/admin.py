from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from editor.models import Topic, Redactor


@admin.register(Redactor)
class RedactorAdmin(UserAdmin):
    empty_value_display = "Absent"
    list_display = UserAdmin.list_display + ("years_of_experience",)
    fieldsets = (
        UserAdmin.fieldsets +
        (("Additional info", {"fields": ("years_of_experience",)}),)
    )
    add_fieldsets = (
        UserAdmin.add_fieldsets +
        (
            (
                "Additional info",
                {
                    "fields": (
                        "first_name",
                        "last_name",
                        "email",
                        "years_of_experience",
                    )
                }
            ),
        )
    )


admin.site.register(Topic)
