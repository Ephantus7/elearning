try:
    from django.conf.urls import url
except ImportError:
    from django.urls import re_path as url

from django.urls import path

from . import StudentExamViews
from . import TeacherExamViews

urlpatterns = [
    path('', StudentExamViews.QuizListView.as_view(), name='student_quiz_index'),
    path('quiz/<slug>/', StudentExamViews.QuizDetailView.as_view(), name='student_quiz_detail'),
    path('quiz/<slug>/take/', StudentExamViews.QuizTake.as_view(), name='student_quiz_take'),
    path('student_progress/', StudentExamViews.QuizUserProgressView.as_view(), name='student_quiz_progress'),
    path('category/', StudentExamViews.CategoriesListView.as_view(), name='student_quiz_category_list_all'),
    path('category/<category_name>/', StudentExamViews.ViewQuizListByCategory.as_view(),
         name='student_quiz_category_list_matching'),
    # url(r'^(?P<slug>[\w-]+)/$', StudentExamViews.QuizDetailView.as_view(), name='student_quiz_start_page'),

    url(r'^(?P<quiz_name>[\w-]+)/take/$', StudentExamViews.QuizTake.as_view(), name='student_quiz_question'),

    path('teacher_all_quizzes/', TeacherExamViews.AllQuizzes.as_view(), name='teacher_all_quizzes'),
    
    url(r'^marking/$', TeacherExamViews.QuizMarkingList.as_view(), name='quiz_marking'),

    url(r'^marking/(?P<pk>[\d.]+)/$', TeacherExamViews.QuizMarkingDetail.as_view(), name='quiz_marking_detail'),
]

# urlpatterns = [
#
#     url(r'^$',
#         view=QuizListView.as_view(),
#         name='quiz_index'),
#
#     url(r'^category/$',
#         view=CategoriesListView.as_view(),
#         name='quiz_category_list_all'),
#
#     url(r'^category/(?P<category_name>[\w|\W-]+)/$',
#         view=ViewQuizListByCategory.as_view(),
#         name='quiz_category_list_matching'),
#
#     url(r'^progress/$',
#         view=QuizUserProgressView.as_view(),
#         name='quiz_progress'),
#
#     url(r'^marking/$',
#         view=QuizMarkingList.as_view(),
#         name='quiz_marking'),
#
#     url(r'^marking/(?P<pk>[\d.]+)/$',
#         view=QuizMarkingDetail.as_view(),
#         name='quiz_marking_detail'),
#
#     #  passes variable 'quiz_name' to quiz_take view
#     url(r'^(?P<slug>[\w-]+)/$',
#         view=QuizDetailView.as_view(),
#         name='quiz_start_page'),
#
#     url(r'^(?P<quiz_name>[\w-]+)/take/$',
#         view=QuizTake.as_view(),
#         name='quiz_question'),
# ]
