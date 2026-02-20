from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, reverse
from django.urls import reverse_lazy

from editor.models import Topic, Newspaper, Redactor


class IndexView(LoginRequiredMixin, generic.View):

    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            "count_topics": Topic.objects.count(),
            "count_newspapers": Newspaper.objects.count(),
            "count_redactors": Redactor.objects.count()
        }
        return render(request, "editor/index.html", context)


class TopicListView(LoginRequiredMixin, generic.ListView):
    model = Topic
    paginate_by = 10


class TopicCreateView(LoginRequiredMixin, generic.CreateView):
    model = Topic
    fields = "__all__"
    success_url = reverse_lazy("editor:topic-list")


class TopicUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Topic
    fields = "__all__"
    success_url = reverse_lazy("editor:topic-list")


class TopicDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Topic
    success_url = reverse_lazy("editor:topic-list")


class NewspaperListView(generic.ListView):
    model = Newspaper
    queryset = Newspaper.objects.prefetch_related("topics")
    paginate_by = 10


class NewspaperDetailView(generic.DetailView):
    model = Newspaper


class NewspaperCreateView(generic.CreateView):
    model = Newspaper
    fields = "__all__"

    def get_success_url(self) -> str:
        return reverse("editor:newspaper-detail", args=[self.object.id])


class NewspaperUpdateView(generic.UpdateView):
    model = Newspaper
    fields = "__all__"

    def get_success_url(self) -> str:
        return reverse("editor:newspaper-detail", args=[self.object.id])


class NewspaperDeleteView(generic.DeleteView):
    model = Newspaper
    success_url = reverse_lazy("editor:newspaper-list")


class RedactorListView(generic.ListView):
    model = Redactor
    paginate_by = 10


class RedactorDetailView(generic.DetailView):
    model = Redactor
    queryset = Redactor.objects.prefetch_related("newspapers__topics")


class RedactorCreateView(generic.CreateView):
    model = Redactor
    fields = "__all__"

    def get_success_url(self) -> str:
        return reverse("editor:redactor-detail", args=[self.object.id])


class RedactorUpdateView(generic.UpdateView):
    model = Redactor
    fields = "__all__"

    def get_success_url(self) -> str:
        return reverse("editor:redactor-detail", args=[self.object.id])


class RedactorDeleteView(generic.DeleteView):
    model = Redactor
    success_url = reverse_lazy("editor:redactor-list")
