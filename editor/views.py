from django.views import generic
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy

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


class TopicCreateView(generic.CreateView):
    model = Topic
    fields = "__all__"
    success_url = reverse_lazy("editor:topic-list")


class TopicUpdateView(generic.UpdateView):
    model = Topic
    fields = "__all__"
    success_url = reverse_lazy("editor:topic-list")


class TopicDeleteView(generic.DeleteView):
    model = Topic
    success_url = reverse_lazy("editor:topic-list")


class NewspaperListView(generic.ListView):
    model = Newspaper
    queryset = Newspaper.objects.prefetch_related("topics")


class NewspaperDetailView(generic.DetailView):
    model = Newspaper


class NewspaperCreateView(generic.CreateView):
    model = Newspaper
    fields = "__all__"
    success_url = reverse_lazy("editor:newspaper-list")


class NewspaperUpdateView(generic.UpdateView):
    model = Newspaper
    fields = "__all__"
    success_url = reverse_lazy("editor:newspaper-list")


class NewspaperDeleteView(generic.DeleteView):
    model = Newspaper
    success_url = reverse_lazy("editor:newspaper-list")
