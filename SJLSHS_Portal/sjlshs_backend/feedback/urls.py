from django.urls import path
from .views import TeacherFeedbackView, FeedbackHomeView, SchoolExperienceFeedbackView, teacher_scores_chart, TeacherChartsView, teacher_feedback_statistics, TeacherStatisticsView

from django_otp.decorators import otp_required



urlpatterns = [
    path('teacher_feedback/', otp_required(TeacherFeedbackView.as_view()), name='teacher-feedback'),
    path('home/', otp_required(FeedbackHomeView.as_view()), name='feedback_home'),
    path('school_experience_feedback/', otp_required(SchoolExperienceFeedbackView.as_view()), name='school-experience-feedback'),
    path('teacher-scores-chart/', otp_required(teacher_scores_chart), name='teacher_scores_chart'),
    path('charts/', TeacherChartsView.as_view(), name='teacher-charts'),
    path('teacher_feedback_statistics/<int:teacher_id>/', teacher_feedback_statistics, name='teacher_feedback_statistics'),
    path('teacher_statistics/', TeacherStatisticsView.as_view(), name='teacher_statistics')
]