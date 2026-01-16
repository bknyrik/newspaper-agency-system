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
        "published_date",
        TopicsListFilter,
        PublishersListFilter
    )
    search_fields = ("title", )

    @admin.display(description="Topics")
    def get_topics(self, newspaper: Newspaper) -> str:
        return ", ".join(str(topic) for topic in newspaper.topics.all())


admin.site.register(Topic)
