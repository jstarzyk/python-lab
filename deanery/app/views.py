from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, FormView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from app.forms import RegistrationForm, MarkForm
from app.models import Student, Teacher, Assignment, Mark


def is_standard_user(user):
    return user.is_authenticated and user.groups.filter(name='standard_user').exists()


def is_admin_user(user):
    return user.is_authenticated and user.groups.filter(name='admin_user').exists()


class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        if not request.user.is_authenticated:
            return redirect(to='/login/')
        if is_standard_user(request.user):
            return redirect(to='/student/')
        elif is_admin_user(request.user):
            return redirect(to='/teacher/')


class CustomLoginView(UserPassesTestMixin, LoginView):
    def test_func(self):
        return not self.request.user.is_authenticated

    def get_login_url(self):
        if is_standard_user(self.request.user):
            return '/student/'
        elif is_admin_user(self.request.user):
            return '/teacher/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Log In'
        return context


class CustomRegisterView(UserPassesTestMixin, FormView):
    form_class = RegistrationForm
    template_name = 'registration/register.html'
    success_url = '/login/'

    def test_func(self):
        return not self.request.user.is_authenticated

    def get_login_url(self):
        return '/home/'

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Account created successfully. You can now log in.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Register'
        return context


class StudentView(UserPassesTestMixin, TemplateView):
    def test_func(self):
        return is_standard_user(self.request.user)

    def get_login_url(self):
        if not self.request.user.is_authenticated:
            return '/login/'
        else:
            return '/teacher/'

    def get(self, request, *args, **kwargs):
        student = Student.objects.get(user=request.user)
        subjects = student.subjects.order_by('name')
        marks = Mark.objects.filter(student=student)
        subject_with_marks_list = []

        for s in subjects:
            m = marks.filter(subject=s).order_by('assignment__name')
            subject_with_marks_list.append({
                'subject': s,
                'marks': m
            })

        return render(request, 'student.html', {
            'full_name': request.user.get_full_name(),
            'title': 'Student',
            'subject_with_marks_list': subject_with_marks_list
        })


class TeacherView(UserPassesTestMixin, TemplateView):
    def test_func(self):
        return is_admin_user(self.request.user)

    def get_login_url(self):
        if not self.request.user.is_authenticated:
            return '/login/'
        else:
            return '/student/'

    def get(self, request, *args, **kwargs):
        subjects = Teacher.objects.get(user=request.user).subjects.order_by('name')
        students = Student.objects.all()
        marks = Mark.objects.all()
        assignments = Assignment.objects.all()
        r_subjects = []

        for subject in subjects:
            r_students = []
            _students = students.filter(subjects__id__exact=subject.id)
            _marks = marks.filter(subject=subject)
            _assignments = assignments.filter(subject=subject).order_by('name')

            for student in _students:
                fm = []
                __marks = _marks.filter(student=student)

                for assignment in _assignments:
                    mark = None
                    if __marks is not None:
                        mark = __marks.filter(assignment=assignment).first()
                    if mark is not None:
                        _mark = mark
                    else:
                        _mark = Mark(
                            subject=subject,
                            assignment=assignment,
                            student=student,
                            value=None
                        )
                    fm.append({
                        'form': MarkForm(instance=_mark),
                        'mark': _mark
                    })

                r_students.append({
                    'full_name': student.user.get_full_name(),
                    'student': student,
                    'fm': fm
                })

            r_subjects.append({
                'name': subject.name,
                'assignments': _assignments,
                'students': r_students
            })

        return render(request, 'teacher.html', {
            'full_name': request.user.get_full_name(),
            'title': 'Teacher',
            'subjects': r_subjects
        })


class UpdateMark(UserPassesTestMixin, UpdateView):
    model = Mark
    success_url = '/teacher/'
    template_name = 'errors.html'
    fields = MarkForm.Meta.fields

    def test_func(self):
        return is_admin_user(self.request.user)

    def get_login_url(self):
        if not self.request.user.is_authenticated:
            return '/login/'
        else:
            return '/student/'


class AddMark(UserPassesTestMixin, CreateView):
    model = Mark
    success_url = '/teacher/'
    template_name = 'errors.html'
    fields = MarkForm.Meta.fields

    def test_func(self):
        return is_admin_user(self.request.user)

    def get_login_url(self):
        if not self.request.user.is_authenticated:
            return '/login/'
        else:
            return '/student/'


class DeleteMark(UserPassesTestMixin, DeleteView):
    model = Mark
    success_url = '/teacher/'
    template_name = 'errors.html'

    def test_func(self):
        return is_admin_user(self.request.user)

    def get_login_url(self):
        if not self.request.user.is_authenticated:
            return '/login/'
        else:
            return '/student/'
