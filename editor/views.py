from django.views import generic
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from editor.models import Topic, Newspaper, Redactor


class IndexView(generic.View):

    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            "count_topics": Topic.objects.count(),
            "count_newspapers": Newspaper.objects.count(),
            "count_redactors": Redactor.objects.count()
        }
        return render(request, "editor/index.html", context)


class TopicListView(generic.ListView):
    model = Topic
