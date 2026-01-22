from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.http import HttpRequest
from django.db.models import QuerySet

from editor.models import Topic, Redactor, Newspaper


class YearsOfExperienceListFilter(admin.SimpleListFilter):
    title = "years of experience"
    parameter_name = "years_of_experience"

    def lookups(
        self,
        request: HttpRequest,
        model_admin: "RedactorAdmin"
    ) -> tuple[tuple[str, str], ...]:
        return (
            ("0", "Absent"),
            ("1,3", "1-3"),
            ("3,5", "3-5"),
            ("5,10", "5-10"),
            ("10,15", "10-15"),
            ("15,20", "15-20"),
            ("20", "20+"),
        )

    def queryset(
        self,
        request: HttpRequest,
        queryset: QuerySet[Redactor]
    ) -> QuerySet[Redactor]:
        if self.value():
            expression = {}
            match self.value():
                case "0":
                    expression["years_of_experience__isnull"] = True
                case "20":
                    expression["years_of_experience__gte"] = 20
                case _:
                    expression["years_of_experience__range"] = tuple(
                        int(year) for year in self.value().split(",")
                    )

            queryset = queryset.filter(**expression)

        return queryset


@admin.register(Redactor)
class RedactorAdmin(UserAdmin):
    empty_value_display = "Absent"
    list_display = UserAdmin.list_display + ("years_of_experience",)
    list_filter = UserAdmin.list_filter + (YearsOfExperienceListFilter,)
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


@admin.register(Newspaper)
class NewspaperAdmin(admin.ModelAdmin):
    empty_value_display = "Absent"
    list_display = ("title", "published_date", "get_topics")
    list_filter = ("published_date", "topics", )

    @admin.display(description="topics")
    def get_topics(self, newspaper: Newspaper) -> str:
        return newspaper.topics_str


admin.site.register(Topic)
