from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group

from app import models


class MarkForm(forms.ModelForm):
    class Meta:
        model = models.Mark
        fields = ['subject', 'assignment', 'student', 'value']
        widgets = {
            'subject': forms.HiddenInput(),
            'assignment': forms.HiddenInput(),
            'student': forms.HiddenInput(),
        }


class RegistrationForm(UserCreationForm):
    first_name = User.first_name
    last_name = User.last_name
    role = forms.ChoiceField(
        label='Role:',
        choices=(
            ('standard_user', 'Student'),
            ('admin_user', 'Teacher'),
        ),
    )

    def save(self, commit=True):
        user = super().save()
        group = Group.objects.get(name=self.cleaned_data['role'])
        user.groups.add(group)
        user.save()
        subjects = models.Subject.objects.all()
        if group.name == 'standard_user':
            student = models.Student.objects.create(user=user)
            student.subjects.add(*subjects)
        elif group.name == 'admin_user':
            models.Teacher.objects.create(user=user)
        return user

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'role')
