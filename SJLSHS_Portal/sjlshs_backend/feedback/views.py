from django.shortcuts import render, redirect
from django.db.models import Avg
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, TemplateView
from .models import TeacherFeedbackModel, SchoolExperienceFeedbackModel
from .forms import TeacherFeedbackForm, SchoolExperienceFeedbackForm
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.db.models import Q

# Create your views here.

@method_decorator(user_passes_test(lambda u: not u.groups.filter(Q(name='Teacher') | Q(name='Advisors')).exists()), name='dispatch')
class TeacherFeedbackView(FormView):
    template_name = 'feedback/teacher_feedback_form.html'
    form_class = TeacherFeedbackForm
    success_url = reverse_lazy('feedback_home')

    def form_valid(self, form):
         feedback = form.save(commit=False)
         feedback.feedback_student = self.request.user
         if TeacherFeedbackModel.objects.filter(feedback_teacher=feedback.feedback_teacher, feedback_student=feedback.feedback_student).exists():
             messages.error(self.request, "You can only provide feedback once for each teacher...")
             print('error')
             return self.form_invalid(form)
         else:
            feedback.save()
            messages.success(self.request, f"Feedback submitted successfully!")
            return super().form_valid(form)
    
from django.db.models import FloatField

from django.db import connection

def teacher_scores_chart(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT accounts_studentuser.username, AVG(teaching_style + learning_activities + teaching_techniques + instructions 
            + classroom_management + fairness_consistency + addressing_behavioral_issues + assessment_feedback 
            + self_reflection_assessment + assessment_techniques + student_support + professionalism 
            + communication + approachability_responsiveness + professional_development) AS overall_score 
            FROM feedback_teacherfeedbackmodel 
            INNER JOIN accounts_studentuser ON accounts_studentuser.id = feedback_teacher_id
            GROUP BY feedback_teacher_id;
        """)
        rows = cursor.fetchall()

        
    teacher_scores = [{'feedback_teacher__username': row[0], 'overall_score': row[1]} for row in rows]
    
    return JsonResponse({'teacher_scores': teacher_scores})


class TeacherChartsView(TemplateView):
     template_name = 'feedback/charts.html'


def teacher_feedback_statistics(request, teacher_id):
    feedback_categories = [
        'teaching_style', 'learning_activities', 'teaching_techniques', 'instructions',
        'classroom_management', 'fairness_consistency', 'addressing_behavioral_issues',
        'assessment_feedback', 'self_reflection_assessment', 'assessment_techniques',
        'student_support', 'professionalism', 'communication', 'approachability_responsiveness',
        'professional_development'
    ]

    # Calculate the average score for each feedback category
    feedback_averages = {}
    for category in feedback_categories:
        feedback_averages[category] = TeacherFeedbackModel.objects.filter(feedback_teacher_id=teacher_id).values(category).aggregate(Avg(category))[
            f'{category}__avg']

    # Return the data in a JSON format
    return JsonResponse(feedback_averages)


class TeacherStatisticsView(TemplateView):
     template_name = 'feedback/teacher_stats_view.html'

     def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['teacher_id'] = self.request.user.id
        return context

@method_decorator(user_passes_test(lambda u: not u.groups.filter(Q(name='Teacher') | Q(name='Advisors')).exists()), name='dispatch')
class FeedbackHomeView(TemplateView):
     template_name = 'feedback/home.html'
     
@method_decorator(user_passes_test(lambda u: not u.groups.filter(Q(name='Teacher') | Q(name='Advisors')).exists()), name='dispatch')
class SchoolExperienceFeedbackView(FormView):
     template_name = 'feedback/school_experience_feedback_form.html'
     form_class = SchoolExperienceFeedbackForm
     success_url = reverse_lazy('feedback_home')

     def form_valid(self, form):
          print("valid form")
          feedback = form.save(commit=False)
          feedback.school_experience_student = self.request.user
          if SchoolExperienceFeedbackModel.objects.filter(school_experience_student=feedback.school_experience_student).exists():
              messages.error(self.request, "You can only provide feedback once.")
              print('error')
              return self.form_invalid(form)
          feedback.save()
          messages.success(self.request, f"Successfully submitted feedback!")
          print("Success!")
          return super().form_valid(form)