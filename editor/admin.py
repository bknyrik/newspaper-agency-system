from django.db.models import QuerySet
from django.http import HttpRequest
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from editor.models import Topic, Newspaper, Redactor


class TopicsListFilter(admin.SimpleListFilter):
    title = _("topics")
    parameter_name = "topic"

    def lookups(
        self,
        request: HttpRequest,
        model_admin: "NewspaperAdmin"
    ) -> tuple[tuple[int, str], ...]:
        return tuple((topic.id, topic.name) for topic in Topic.objects.all())

    def queryset(
        self,
        request: HttpRequest,
        queryset: QuerySet[Newspaper]
    ) -> QuerySet[Newspaper]:
        if self.value():
            return queryset.filter(topics__id=self.value())

        return queryset.all()


class PublishersListFilter(admin.SimpleListFilter):
    title = _("publishers")
    parameter_name = "publisher"

    def lookups(
        self,
        request: HttpRequest,
        model_admin: "NewspaperAdmin"
    ) -> tuple[tuple[int, str], ...]:
        return tuple(
            (redactor.id, str(redactor))
            for redactor in Redactor.objects.all()
        )

    def queryset(
        self,
        request: HttpRequest,
        queryset: QuerySet[Newspaper]
    ) -> QuerySet[Newspaper]:
        if self.value():
            return queryset.filter(publishers__id=self.value())

        return queryset.all()


class YearsOfExperienceListFilter(admin.SimpleListFilter):
    title = "years of experience"
    parameter_name = "years_of_experience"

    def lookups(
        self,
        request: HttpRequest,
        model_admin: "RedactorAdmin"
    ) -> tuple[tuple[str, str], ...]:
        return (
            ("0,2", "0-2"),
            ("2,5", "2-5"),
            ("5,10", "5-10"),
            ("10,15", "10-15"),
            ("15,20", "15-20"),
            ("20", "20+")
        )

    def queryset(
        self,
        request: HttpRequest,
        queryset: QuerySet[Redactor]
    ) -> QuerySet[Redactor]:
        if self.value():
            if self.value() == "20":
                queryset = queryset.filter(
                    years_of_experience__gte=20
                )
            else:
                queryset = queryset.filter(
                    years_of_experience__range=tuple(
                        int(years) for years in self.value().split(",")
                    )
                )

        return queryset


@admin.register(Redactor)
class RedactorAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("years_of_experience",)
    list_filter = UserAdmin.list_filter + (YearsOfExperienceListFilter, )
    fieldsets = UserAdmin.fieldsets + (
        (
            "Additional info",
            {"fields": ("years_of_experience", )}
        ),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Additional info",
            {"fields": ("first_name", "last_name", "email", "years_of_experience")}
        ),
    )


@admin.register(Newspaper)
class NewspaperAdmin(admin.ModelAdmin):
    list_display = ("title", "published_date", "get_topics")
    list_filter = (
        "published_date",
        TopicsListFilter,
        PublishersListFilter
    )
    search_fields = ("title", )

    @admin.display(description="Topics")
    def get_topics(self, newspaper: Newspaper) -> str:
        return ", ".join(str(topic) for topic in newspaper.topics.all())


admin.site.register(Topic)
