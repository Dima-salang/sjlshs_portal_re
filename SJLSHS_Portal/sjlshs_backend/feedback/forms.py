from django import forms
from .models import TeacherFeedbackModel, SchoolExperienceFeedbackModel
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.core.exceptions import ValidationError



User = get_user_model()

class TeacherFeedbackForm(forms.ModelForm):

    class Meta:
        model = TeacherFeedbackModel
        exclude = ['feedback_student', 'created_at']
        widgets = {
            'teaching_style': forms.RadioSelect,
            'learning_activities': forms.RadioSelect,
            'teaching_techniques': forms.RadioSelect,
            'instructions': forms.RadioSelect,
            'classroom_management': forms.RadioSelect,
            'fairness_consistency': forms.RadioSelect,
            'addressing_behavioral_issues': forms.RadioSelect,
            'assessment_feedback': forms.RadioSelect,
            'self_reflection_assessment': forms.RadioSelect,
            'assessment_techniques': forms.RadioSelect,
            'student_support': forms.RadioSelect,
            'professionalism': forms.RadioSelect,
            'communication': forms.RadioSelect,
            'approachability_responsiveness': forms.RadioSelect,
            'professional_development': forms.RadioSelect,
        }

    def clean(self):
        cleaned_data = super().clean()
        feedback_teacher = cleaned_data.get('feedback_teacher')
        feedback_student = cleaned_data.get('feedback_student')
        if TeacherFeedbackModel.objects.filter(feedback_teacher=feedback_teacher, feedback_student=feedback_student).exists():
            raise ValidationError('You have already submitted feedback for this teacher')
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['feedback_teacher'].queryset = User.objects.filter(Q(groups__name='Teacher') | Q(groups__name='Advisors')).distinct()


class SchoolExperienceFeedbackForm(forms.ModelForm):

    class Meta:
        model = SchoolExperienceFeedbackModel
        exclude = ['created_at']
        widgets = {
            'cleanliness_and_maintenance_facilities_cleanliness': forms.RadioSelect,
            'cleanliness_and_maintenance_school_grounds_appearance': forms.RadioSelect,
            'cleanliness_and_maintenance_bathroom_maintenance': forms.RadioSelect,
            'cleanliness_and_maintenance_building_equipment_maintenance': forms.RadioSelect,
            'safety_and_security_safe_environment': forms.RadioSelect,
            'safety_and_security_safety_measures': forms.RadioSelect,
            'safety_and_security_communication_of_safety_procedures': forms.RadioSelect,
            'safety_and_security_response_to_safety_concerns': forms.RadioSelect,
            'service_and_support_friendly_staff': forms.RadioSelect,
            'service_and_support_support_services_for_students': forms.RadioSelect,
            'service_and_support_parent_communication': forms.RadioSelect,
            'service_and_support_appropriate_resources_for_students': forms.RadioSelect,
            'academic_experience_challenging_program': forms.RadioSelect,
            'academic_experience_extracurricular_activities': forms.RadioSelect,
            'academic_experience_effective_communication': forms.RadioSelect,
            'overall_experience_positive_experience': forms.RadioSelect,
            'overall_experience_quality_education': forms.RadioSelect,
            'overall_experience_diversity_and_inclusion': forms.RadioSelect,
            'overall_experience_recommendation_to_others': forms.RadioSelect,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['school_experience_student'].queryset = User.objects.exclude(Q(groups__name='Teacher') | Q(groups__name='Advisors'))

