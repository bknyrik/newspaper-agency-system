from django import forms

from editor.models import Topic, Newspaper


class TopicForm(forms.ModelForm):

    newspapers = forms.ModelMultipleChoiceField(
        queryset=Newspaper.objects.prefetch_related("topics"),
        widget=forms.SelectMultiple,
        required=False,
    )

    class Meta:
        model = Topic
        fields = ("name", "newspapers")

    def save(self, commit: bool = ...) -> Topic:
        topic = super().save(commit=False)

        if commit:
            topic.save()

        self.save_m2m()
        topic.newspapers.set(self.cleaned_data["newspapers"])
        return topic
