import datetime
from datetime import datetime
from datetime import datetime as dt

from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView

from .forms import AssignmentUploadForm
from .models import Student, CustomUser, Assignment, Book, Video, PastPaper, AssignmentUploads, \
    AssignmentScores, AssignmentCategory


def not_a_student(user):
    if user.user_type == 3:
        return True
    return False


class StudentRequiredMixin(object):
    @method_decorator(user_passes_test(not_a_student, login_url='login'))
    def dispatch(self, request, *args, **kwargs):
        return super(StudentRequiredMixin, self).dispatch(request, *args, **kwargs)  # type: ignore


class StudentHomeView(LoginRequiredMixin, StudentRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(CustomUser, id=request.user.id)
        student = get_object_or_404(Student, user=request.user.id)

        assignments = Assignment.objects.filter(Q(subject__course__student=student)
                                                & Q(created_at__lte=dt.now())
                                                & Q(deadline_date__lte=dt.now().date())
                                                & Q(deadline_time__lt=dt.now().time())
                                                & ~Q(assignmentuploads__student=student)
                                                ).order_by('-created_at')[:3]

        books = Book.objects.filter(subject__course__student=student)
        videos = Video.objects.filter(subject__course__student=student)
        papers = PastPaper.objects.filter(subject__course__student=student)

        recent_books = Book.objects.filter(subject__course__student=student) \
                           .filter(date_added__lte=dt.now()) \
                           .order_by('-date_added')[:3]

        recent_papers = PastPaper.objects.filter(subject__course__student=student) \
                            .filter(date_added__lte=dt.now()) \
                            .order_by('-date_added')[:3]

        recent_assignments = assignments

        recent_videos = Video.objects.filter(subject__course__student=student) \
                            .filter(date_added__lte=dt.now()) \
                            .order_by('-date_added')[:3]

        context = {
            'student': student,
            'assignments': assignments,
            'books': books,
            'videos': videos,
            'papers': papers,
            'user': user,
            'recent_books': recent_books,
            'recent_papers': recent_papers,
            'recent_assignments': recent_assignments,
            'recent_videos': recent_videos,
        }

        return render(request, 'students/student_home.html', context)


class StudentBookViews(LoginRequiredMixin, StudentRequiredMixin, ListView):
    model = Book
    paginate_by = 10

    template_name = 'students/student_books.html'

    def get(self, request, *args, **kwargs):
        student = get_object_or_404(Student, user=request.user.id)

        books = Book.objects.filter(subject__course__student=student)

        return render(request, 'students/student_books.html', {'books': books})


class StudentVideoViews(LoginRequiredMixin, StudentRequiredMixin, ListView):
    template_name = 'students/student_videos.html'
    model = Video

    def get(self, request, *args, **kwargs):
        student = get_object_or_404(Student, user=request.user.id)

        videos = Video.objects.filter(subject__course__student=student)

        return render(request, 'students/student_videos.html', {'videos': videos})


class StudentPaperViews(LoginRequiredMixin, StudentRequiredMixin, ListView):
    model = PastPaper
    template_name = 'students/student_papers.html'

    def get(self, request, *args, **kwargs):
        student = get_object_or_404(Student, user=request.user.id)

        papers = PastPaper.objects.filter(subject__course__student=student)
        return render(request, 'students/student_papers.html', {'papers': papers})


class StudentAssignmentViews(LoginRequiredMixin, StudentRequiredMixin, ListView):

    def get(self, request, *args, **kwargs):
        form = AssignmentUploadForm()
        student = get_object_or_404(Student, user=request.user.id)
        assignments = Assignment.objects.filter(Q(subject__course__student=student)
                                                & Q(created_at__lte=dt.now())
                                                & Q(deadline_date__lte=dt.now().date())
                                                & Q(deadline_time__lt=dt.now().time())
                                                & ~Q(assignmentuploads__student=student)
                                                ).order_by('-created_at')

        context = {
            'assignments': assignments,
            'form': form
        }
        return render(request, 'students/student_assignments.html', context)

    def post(self, request, *args, **kwargs):
        form = AssignmentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            assignment = Assignment.objects.get(id=request.POST['assignment_id'])
            student = get_object_or_404(Student, user=request.user.id)
            try:
                already_uploaded = AssignmentUploads.objects.get(assignment=assignment, student=student)
                already_uploaded.finished_assignment_file = request.FILES['finished_assignment_file']
                already_uploaded.save()
            except AssignmentUploads.DoesNotExist:
                AssignmentUploads.objects.create(
                    assignment=assignment,
                    student=student,
                    finished_assignment_file=request.FILES['finished_assignment_file'],
                )

            messages.success(request, 'Assignment uploaded successfully')
            return HttpResponseRedirect('/past_assignments/')
        else:
            return HttpResponseRedirect(reverse_lazy('student_assignments'))


class PastAssignmentView(LoginRequiredMixin, StudentRequiredMixin, ListView):
    def get(self, request, *args, **kwargs):
        student = get_object_or_404(Student, user=request.user.id)
        assignments = Assignment.objects.filter(subject__course__student=student) \
            .filter(assignmentuploads__student=student).order_by('-created_at')

        context = {
            'assignments': assignments,
        }
        return render(request, 'students/past_assignments.html', context)


class StudentAssignmentResultsViews(LoginRequiredMixin, StudentRequiredMixin, ListView):
    model = AssignmentScores
    template_name = 'students/student_assignment_results.html'

    def get(self, request, *args, **kwargs):
        student = get_object_or_404(Student, user=request.user.id)
        assignments = Assignment.objects.filter(subject__course__student=student)
        categories = AssignmentCategory.objects.all()
        uploads = AssignmentUploads.objects.filter(assignment__in=assignments) \
            .filter(student=student)
        scores = AssignmentScores.objects.filter(assignment__in=assignments) \
            .filter(student=student)

        context = {
            'assignments': assignments,
            'uploads': uploads,
            'scores': scores,
            'categories': categories,
        }

        return render(request, self.template_name, context)


class StudentExamViews(LoginRequiredMixin, StudentRequiredMixin, ListView):
    def get(self, request, *args, **kwargs):
        user = get_object_or_404(CustomUser, id=request.user.id)

        return render(request, 'students/student_exams.html')


class StudentCatViews(LoginRequiredMixin, StudentRequiredMixin, ListView):

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(CustomUser, id=request.user.id)

        return render(request, 'students/student_cats.html')


class StudentExamResultViews(LoginRequiredMixin, StudentRequiredMixin, ListView):

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(CustomUser, id=request.user.id)

        return render(request, 'students/student_exams_results.html')


class StudentExtraResultViews(LoginRequiredMixin, StudentRequiredMixin, ListView):

    def get(self, request, *args, **kwargs):
        return render(request, 'students/student_extra_results.html')
