from django.urls import path
from .views import HomePageView, ProfilePageView, SignupView, CoursesView,  \
    DashboardView, ContactView, StudentProfileView, TeacherProfileView, UserPasswordChangeView
from . import StudentViews
from . import TeacherViews


urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('student_home/', StudentViews.StudentHomeView.as_view(), name='student_home'),
    path('accounts/profile/', ProfilePageView.as_view(), name='profile'),
    path('accounts/password_change/', UserPasswordChangeView.as_view(), name='password_change'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('student_books/', StudentViews.StudentBookViews.as_view(), name='student_books'),
    path('student_videos/', StudentViews.StudentVideoViews.as_view(), name='student_videos'),
    path('student_papers/', StudentViews.StudentPaperViews.as_view(), name='student_papers'),
    path('student_exams/', StudentViews.StudentExamViews.as_view(), name='student_exams'),
    path('student_cats/', StudentViews.StudentCatViews.as_view(), name='student_cats'),
    path('student_assignments/', StudentViews.StudentAssignmentViews.as_view(), name='student_assignments'),
    path('student_exams_results/', StudentViews.StudentExamResultViews.as_view(), name='student_exams_results'),
    path('student_extra/', StudentViews.StudentExtraResultViews.as_view(), name='student_extra'),
    path('teacher_home/', TeacherViews.TeacherHomeView.as_view(), name='teacher_home'),
    path('teacher_exams/', TeacherViews.TeacherExamViews.as_view(), name='teacher_exams'),
    path('teacher_cats/', TeacherViews.TeacherCATViews.as_view(), name='teacher_cats'),
    path('teacher_assignments/', TeacherViews.TeacherAssignmentViews.as_view(), name='teacher_assignments'),
    path('teacher_exams_results/', TeacherViews.TeacherExamResultsViews.as_view(), name='teacher_exams_results'),
    path('past_assignments/', StudentViews.PastAssignmentView.as_view(), name='past_assignments'),
    path('teacher_assignment_details/<int:pk>/', TeacherViews.TeacherAssignmentDetailView.as_view(), name='teacher_assignment_details'),
    path('student_assignment_results', StudentViews.StudentAssignmentResultsViews.as_view(), name='student_assignment_results'),
    # path('courses/' , CoursesView.as_view(), name='courses'),
    # path('course_details/<int:pk>/', CourseDetailView.as_view(), name='course_details'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('student_profile/<int:pk>/', StudentProfileView.as_view(), name='student_profile'),
    path('teacher_profile/<int:pk>/', TeacherProfileView.as_view(), name='teacher_profile'),
    path('teacher_books/', TeacherViews.TeacherBookViews.as_view(), name='teacher_books'),
    path('teacher_papers/', TeacherViews.TeacherPaperViews.as_view(), name='teacher_papers'),
    path('teacher_videos/', TeacherViews.TeacherVideoViews.as_view(), name='teacher_videos'),
]
