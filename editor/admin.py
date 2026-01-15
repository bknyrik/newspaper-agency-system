from django.contrib import admin

from editor.models import Topic, Newspaper


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

    def get_topics(self, newspaper: Newspaper) -> str:
        return ", ".join(str(topic) for topic in newspaper.topics.all())


admin.site.register(Topic)
