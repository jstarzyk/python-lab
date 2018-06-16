from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group


class RegistrationForm(UserCreationForm):
    first_name = User.first_name
    last_name = User.last_name
    role = forms.ChoiceField(
        label='Role:',
        choices=(
            ('standard_user', 'Student'),
            ('admin_user', 'Teacher')
        ),
    )

    def clean_first_name(self):
        return self.cleaned_data['first_name']

    def clean_last_name(self):
        return self.cleaned_data['last_name']

    def clean_role(self):
        return self.cleaned_data['role']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['username']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.groups.add(Group.objects.get(name=self.cleaned_data['role']))
        user.save()
        # return user

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'role')
        # labels =

        # user = User.objects.create_user(
        #     username=self.cleaned_data['username'],
        #     password=self.cleaned_data['password1'],
        #     first_name=self.cleaned_data['first_name'],
        #     last_name=self.cleaned_data['last_name']
        # )
        # return user
        # user.first_name = f
