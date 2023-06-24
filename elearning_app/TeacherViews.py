from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView, DetailView

from .forms import AssignmentScoreForm, NewAssignmentForm, NewBookForm, NewPastPaperForm, NewVideoForm
from .models import *


def not_a_teacher(user):
    if user.user_type == 2:
        return True
    return False


class TeacherRequiredMixin(object):
    @method_decorator(user_passes_test(not_a_teacher, login_url='login'))
    def dispatch(self, request, *args, **kwargs):
        return super(TeacherRequiredMixin, self).dispatch(request, *args, *kwargs) # type: ignore


class TeacherHomeView(LoginRequiredMixin, TeacherRequiredMixin, TemplateView):
    template_name = 'teachers/teacher_home.html'

    def get(self, request, *args, **kwargs):
        teacher = get_object_or_404(Teacher, user=request.user.id)
        assignments = Assignment.objects.filter(created_by=teacher)
        books = Book.objects.filter(added_by=teacher)
        papers = PastPaper.objects.filter(added_by=teacher)
        videos = Video.objects.filter(added_by=teacher)

        recent_assignments = Assignment.objects.filter(created_by=teacher) \
            .filter(created_at__lte=datetime.now()) \
                    .order_by('-created_at')[:3]

        recent_assignment_uploads = AssignmentUploads.objects.filter(
            Q(assignment__created_by=teacher) \
                & Q(assignment__created_at__lte=datetime.now()) \
                    & Q(assignmentscores__isnull=True) \
        )

        recent_papers = PastPaper.objects.filter(added_by=teacher) \
            .filter(date_added__lte=datetime.now()) \
                    .order_by('-date_added')[:3]

        recent_books = Book.objects.filter(added_by=teacher) \
            .filter(date_added__lte=datetime.now()) \
                    .order_by('-date_added')[:3]

        recent_videos = Video.objects.filter(added_by=teacher) \
            .filter(date_added__lte=datetime.now()) \
                    .order_by('-date_added')[:3]

        context = {
            'recent_assignments': recent_assignments,
            'recent_assignment_uploads': recent_assignment_uploads,
            'recent_papers': recent_papers,
            'recent_videos': recent_videos,
            'recent_books': recent_books,
            'assignments': assignments,
            'videos': videos,
            'books': books,
            'papers': papers,
            'teacher': teacher,
        }

        return render(request, self.template_name, context)


class TeacherBookViews(LoginRequiredMixin, TeacherRequiredMixin, ListView):
    model = Book
    paginate_by = 10

    template_name = 'teachers/teacher_books.html'

    def get(self, request, *args, **kwargs):
        form = NewBookForm()
        teacher = get_object_or_404(Teacher, user=request.user.id)

        books = Book.objects.filter(added_by=teacher)

        return render(request, 'teachers/teacher_books.html', {'books': books, 'form':form})

    def post(self, request, *args, **kwargs):
        form = NewBookForm(request.POST, request.FILES)
        teacher = get_object_or_404(Teacher, user=request.user.id)

        if form.is_valid():
            form.save(commit=False)
            form.instance.added_by = teacher
            form.save()

            messages.success(request, 'Book added successfully')
            return redirect('teacher_books')

        messages.error(request, 'Book not added')
        return redirect('teacher_books')


class TeacherPaperViews(LoginRequiredMixin, TeacherRequiredMixin, ListView):
    model = PastPaper
    template_name = 'teachers/teacher_papers.html'

    def get(self, request, *args, **kwargs):
        form = NewPastPaperForm()
        teacher = get_object_or_404(Teacher, user=request.user.id)

        papers = PastPaper.objects.filter(added_by=teacher)

        return render(request, self.template_name, {'papers': papers, 'form':form})

    def post(self, request, *args, **kwargs):
        form = NewPastPaperForm(request.POST, request.FILES)
        teacher = get_object_or_404(Teacher, user=request.user.id)

        if form.is_valid():
            form.save(commit=False)
            form.instance.added_by = teacher
            form.save()

            messages.success(request, 'Past paper added successfully')
            return redirect('teacher_papers')

        messages.error(request, 'Past paper not added')
        return redirect('teacher_papers')


class TeacherVideoViews(LoginRequiredMixin, TeacherRequiredMixin, ListView):
    model = Video
    template_name = 'teachers/teacher_videos.html'

    def get(self, request, *args, **kwargs):
        form = NewVideoForm()
        teacher = get_object_or_404(Teacher, user=request.user.id)

        videos = Video.objects.filter(added_by=teacher)

        return render(request, self.template_name, {'videos': videos, 'form':form})

    def post(self, request, *args, **kwargs):
        form = NewVideoForm(request.POST)
        teacher = get_object_or_404(Teacher, user=request.user.id)

        if form.is_valid():
            form.save(commit=False)
            form.instance.added_by = teacher
            form.save()

            messages.success(request, 'Video added successfully')
            return redirect('teacher_videos')

        messages.error(request, 'Video not added')
        return redirect('teacher_videos')


class TeacherExamViews(LoginRequiredMixin, TeacherRequiredMixin, TemplateView):
    template_name = 'teachers/teacher_exams.html'


class TeacherCATViews(LoginRequiredMixin, TeacherRequiredMixin, TemplateView):
    template_name = 'teachers/teacher_cats.html'


class TeacherAssignmentViews(LoginRequiredMixin, TeacherRequiredMixin, TemplateView):
    template_name = 'teachers/teacher_assignments.html'

    def get(self, request, *args, **kwargs):
        form = NewAssignmentForm()
        teacher = get_object_or_404(Teacher, user=request.user.id)

        assignments = Assignment.objects.filter(
            Q(created_by=teacher)
        )

        context = {
            'assignments': assignments,
            'form': form,
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = NewAssignmentForm(request.POST, request.FILES)
        teacher = get_object_or_404(Teacher, user=request.user.id)

        if form.is_valid():
            form.save(commit=False)
            form.instance.created_by = teacher
            form.save()

            messages.success(request, 'Assignment created successfully')
            return redirect('teacher_assignments')

        messages.error(request, 'Assignment not created')
        return redirect('teacher_assignments')


class TeacherAssignmentDetailView(LoginRequiredMixin, TeacherRequiredMixin, DetailView):
    model = Assignment
    template_name = 'teachers/teacher_assignment_details.html'

    def get(self, request, *args, **kwargs):
        teacher = get_object_or_404(Teacher, user=request.user.id)

        assignments = Assignment.objects.filter(
            Q(created_by=teacher) \
                & Q(assignmentuploads__isnull=False) \
                    & Q(assignmentscores__isnull=True) \
        ).order_by('-created_at')

        uploads = AssignmentUploads.objects.filter(
            Q (assignment__created_by=teacher) \
                & Q(assignment__id=self.kwargs['pk']) \
                    & Q(assignmentscores__score__isnull=True) \
        ).order_by('-date_uploaded')

        form = AssignmentScoreForm()

        context = {
            'assignments': assignments,
            'uploads': uploads,
            'form': form
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = AssignmentScoreForm(request.POST)

        if form.is_valid():
            score = form.cleaned_data['score']
            teacher = get_object_or_404(Teacher, user=request.user.id)

            assignment = Assignment.objects.get(id=self.kwargs['pk'])

            uploads = AssignmentUploads.objects.filter(
                Q(assignment__created_by=teacher) \
                    & Q(assignment__id=self.kwargs['pk']) \
                        & Q(assignmentscores__score__isnull=True) \
            ).order_by('-date_uploaded')

            for upload in uploads:
                if score is not None:
                    student = upload.student

                    assignment_score = AssignmentScores.objects.create(
                        assignment=assignment,
                        student=student,
                        upload=upload,
                        scored_by=teacher,
                        score=score,
                    )

                    assignment_score.save()

                messages.success(request, 'Assignment score added successfully')
                return redirect('teacher_assignment_details', pk=self.kwargs['pk'])

            messages.error(request, 'Assignment score not added')
            return redirect('teacher_assignment_details', pk=self.kwargs['pk'])

        messages.error(request, 'Assignment score not added')
        return redirect('teacher_assignment_details', pk=self.kwargs['pk'])


class TeacherExamResultsViews(LoginRequiredMixin, TeacherRequiredMixin, TemplateView):
    template_name = 'teachers/teacher_exams_results.html'
