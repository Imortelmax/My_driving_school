from django import forms
from .models import Lesson, Package, User, LessonRequest

class CreateUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'role']


class EditUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False, help_text="Leave blank to keep current password")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'role']

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user


class LessonForm(forms.ModelForm):
    date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        input_formats=['%Y-%m-%dT%H:%M']
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['student'].queryset = User.objects.filter(role='student')
        self.fields['instructor'].queryset = User.objects.filter(role='instructor')

    class Meta:
        model = Lesson
        fields = ['student', 'instructor', 'date', 'location', 'duration']


class PackageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['student'].queryset = User.objects.filter(role='student')

    class Meta:
        model = Package
        fields = ['student', 'hours_total']

class StudentPackageForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = ['hours_total']
        labels = {'hours_total': 'Number of hours'}


class LessonRequestForm(forms.ModelForm):
    date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        input_formats=['%Y-%m-%dT%H:%M']
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['instructor'].queryset = User.objects.filter(role='instructor')

    class Meta:
        model = LessonRequest
        fields = ['instructor', 'date', 'location', 'duration']


class CounterProposalForm(forms.Form):
    date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        input_formats=['%Y-%m-%dT%H:%M']
    )
    location = forms.CharField(max_length=100)
    duration = forms.IntegerField(min_value=1)