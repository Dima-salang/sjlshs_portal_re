from django.urls import path
from . import views
from django_otp.views import LoginView
from django_otp.forms import OTPTokenForm, OTPAuthenticationForm


# url patterns
urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('signup/redirect/', views.SignUpRedirectView.as_view(), name='signup-redirect'),
    path('password/reset/', views.forgot_password_view, name='forgot-password'),
    path('password/reset/<str:token>/', views.reset_password, name='reset_password'),
    path('activate/<uidb64>/<token>', views.SignUpView.activate, name='activate'),
    path('teachers/dashboard/', views.TeacherDashboardView, name='tc-dashboard'),
    path('teachers/view/student-info<int:uid>', views.StudentInfoView, name='student-info'),
    path('teachers/registration/', views.TeacherRegistrationView.as_view(), name='teacher-registration'),
    path('teachers/login', views.TeacherLogInView.as_view(), name='teacher-login'),
    path('teachers/change_details/', views.teacher_change_details, name='teacher-change-details'),
    path('teachers/update_password/', views.UpdatePassword.as_view(), name='teacher-update-password'),
]