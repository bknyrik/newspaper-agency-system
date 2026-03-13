from django.db.models import QuerySet
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, reverse, get_object_or_404
from django.urls import reverse_lazy

from editor.models import Topic, Newspaper, Redactor
from editor.forms import (
    TopicForm,
    RedactorCreationForm,
    RedactorUpdateForm,
    TopicSearchForm
)


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

    def get_context_data(self, *, object_list = ..., **kwargs) -> dict:
        context = super(TopicListView, self).get_context_data(**kwargs)
        context["search_form"] = TopicSearchForm(self.request.GET)
        return context

    def get_queryset(self) -> QuerySet[Topic]:
        queryset = Topic.objects.all()
        name = self.request.GET.get("name", "")
        search_form = TopicSearchForm(self.request.GET)

        if search_form.is_valid():
            queryset = queryset.filter(name__icontains=name)

        return queryset


class TopicCreateView(LoginRequiredMixin, generic.CreateView):
    model = Topic
    form_class = TopicForm
    success_url = reverse_lazy("editor:topic-list")


class TopicUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Topic
    form_class = TopicForm
    success_url = reverse_lazy("editor:topic-list")


class TopicDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Topic
    success_url = reverse_lazy("editor:topic-list")


class NewspaperListView(LoginRequiredMixin, generic.ListView):
    model = Newspaper
    queryset = Newspaper.objects.prefetch_related("topics")
    paginate_by = 10


class NewspaperDetailView(LoginRequiredMixin, generic.DetailView):
    model = Newspaper

    def post(
        self,
        request: HttpRequest,
        *args,
        **kwargs
    ) -> HttpResponseRedirect:
        newspaper = get_object_or_404(Newspaper, pk=kwargs["pk"])
        redactor = request.user

        if redactor in newspaper.publishers.all():
            newspaper.publishers.remove(redactor.id)
        else:
            newspaper.publishers.add(redactor.id)

        return HttpResponseRedirect(
            reverse("editor:newspaper-detail", args=[kwargs["pk"]])
        )


class NewspaperCreateView(LoginRequiredMixin, generic.CreateView):
    model = Newspaper
    fields = "__all__"

    def get_success_url(self) -> str:
        return reverse("editor:newspaper-detail", args=[self.object.id])


class NewspaperUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Newspaper
    fields = "__all__"

    def get_success_url(self) -> str:
        return reverse("editor:newspaper-detail", args=[self.object.id])


class NewspaperDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Newspaper
    success_url = reverse_lazy("editor:newspaper-list")


class RedactorListView(LoginRequiredMixin, generic.ListView):
    model = Redactor
    paginate_by = 10


class RedactorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Redactor
    queryset = Redactor.objects.prefetch_related("newspapers__topics")


class RedactorCreateView(LoginRequiredMixin, generic.CreateView):
    model = Redactor
    form_class = RedactorCreationForm

    def get_success_url(self) -> str:
        return reverse("editor:redactor-detail", args=[self.object.id])


class RedactorUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Redactor
    form_class = RedactorUpdateForm

    def get_success_url(self) -> str:
        return reverse("editor:redactor-detail", args=[self.object.id])


class RedactorDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Redactor
    success_url = reverse_lazy("editor:redactor-list")
