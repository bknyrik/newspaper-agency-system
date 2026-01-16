from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from editor.models import Topic, Newspaper, Redactor


@admin.register(Redactor)
class RedactorAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("years_of_experience",)
    list_filter = UserAdmin.list_filter + ("years_of_experience", )
    fieldsets = UserAdmin.fieldsets + (
        (
            "Additional info",
            {"fields": ("years_of_experience", )}
        ),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Additional info",
            {"fields": ("first_name", "last_name", "years_of_experience")}
        ),
    )


@admin.register(Newspaper)
class NewspaperAdmin(admin.ModelAdmin):
    list_display = ("title", "published_date", "get_topics")
    list_filter = (
        "title",
        "published_date",
        "topics",
        "publishers__username"
    )
    search_fields = ("title", )

    @admin.display(description="Topics")
    def get_topics(self, newspaper: Newspaper) -> str:
        return ", ".join(str(topic) for topic in newspaper.topics.all())


admin.site.register(Topic)
