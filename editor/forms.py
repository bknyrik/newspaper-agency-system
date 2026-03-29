from django import forms
from django.contrib.auth.forms import UserCreationForm

from editor.models import Topic, Newspaper, Redactor


class TopicForm(forms.ModelForm):

    newspapers = forms.ModelMultipleChoiceField(
        queryset=Newspaper.objects.prefetch_related("topics"),
        required=False,
    )

    class Meta:
        model = Topic
        fields = ("name", "newspapers")

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["newspapers"].initial = (
                self.instance.newspapers.all()
            )

    def save(self, commit: bool = ...) -> Topic:
        topic = super().save(commit=False)

        if commit:
            topic.save()

        self.save_m2m()
        topic.newspapers.set(self.cleaned_data["newspapers"])
        return topic


class TopicSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by name"}
        )
    )


class NewspaperSearchForm(forms.Form):
    title = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by title"})
    )


class RedactorCreationForm(UserCreationForm):

    years_of_experience = forms.IntegerField(min_value=1, required=False)
    newspapers = forms.ModelMultipleChoiceField(
        queryset=Newspaper.objects.prefetch_related("topics"),
        required=False
    )

    class Meta(UserCreationForm.Meta):

        model = Redactor
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "email",
            "years_of_experience",
            "newspapers"
        )

    def save(self, commit: bool = ...) -> Redactor:
        redactor = super().save(commit=False)

        if commit:
            redactor.save()

        self.save_m2m()
        redactor.newspapers.set(self.cleaned_data["newspapers"])
        return redactor


class RedactorUpdateForm(forms.ModelForm):

    years_of_experience = forms.IntegerField(min_value=1, required=False)
    newspapers = forms.ModelMultipleChoiceField(
        queryset=Newspaper.objects.prefetch_related("topics"),
        required=False
    )

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["newspapers"].initial = (
                self.instance.newspapers.all()
            )

    class Meta:
        model = Redactor
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "years_of_experience",
            "newspapers"
        )

    def save(self, commit: bool = ...) -> Redactor:
        redactor = super().save(commit=False)

        if commit:
            redactor.save()

        self.save_m2m()
        redactor.newspapers.set(self.cleaned_data["newspapers"])
        return redactor


class RedactorSearchForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        label="",
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Search by username"}
        )
    )
    years_of_experience = forms.IntegerField(
        min_value=1,
        required=False,
        label="",
        widget=forms.NumberInput(
            attrs={
                "class": "mt-3",
                "placeholder": "Search by years of experience"
            }
        )
    )
