from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class TeacherFeedbackModel(models.Model):

    feedback_rating = (
        (1, "Poor"),
        (2, "Below Average"),
        (3, "Average"),
        (4, "Good"),
        (5, "Excellent")
    )

    feedback_teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedback_teacher', verbose_name="Teacher")
    feedback_student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedback_student')
    teaching_style = models.IntegerField(choices=feedback_rating)
    learning_activities = models.IntegerField(choices=feedback_rating)
    teaching_techniques = models.IntegerField(choices=feedback_rating)
    instructions = models.IntegerField(choices=feedback_rating)
    classroom_management = models.IntegerField(choices=feedback_rating)
    fairness_consistency = models.IntegerField(choices=feedback_rating)
    addressing_behavioral_issues = models.IntegerField(choices=feedback_rating)
    assessment_feedback = models.IntegerField(choices=feedback_rating)
    self_reflection_assessment = models.IntegerField(choices=feedback_rating)
    assessment_techniques = models.IntegerField(choices=feedback_rating)
    student_support = models.IntegerField(choices=feedback_rating)
    professionalism = models.IntegerField(choices=feedback_rating)
    communication = models.IntegerField(choices=feedback_rating)
    approachability_responsiveness = models.IntegerField(choices=feedback_rating)
    professional_development = models.IntegerField(choices=feedback_rating)
    additional_comments = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


    # ensures that student can only leave feedback for a teacher once by putting a unique constraint on the combination.
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['feedback_teacher', 'feedback_student'], name='unique_teacher_feedback')
        ]


class SchoolExperienceFeedbackModel(models.Model):
    
    feedback_rating = (
        (1, "Poor"),
        (2, "Below Average"),
        (3, "Average"),
        (4, "Good"),
        (5, "Excellent")
    )

    school_experience_student = models.ForeignKey(User, on_delete=models.CASCADE)

    cleanliness_and_maintenance_facilities_cleanliness = models.IntegerField(choices=feedback_rating)
    cleanliness_and_maintenance_school_grounds_appearance = models.IntegerField(choices=feedback_rating)
    cleanliness_and_maintenance_bathroom_maintenance = models.IntegerField(choices=feedback_rating)
    cleanliness_and_maintenance_building_equipment_maintenance = models.IntegerField(choices=feedback_rating)

    safety_and_security_safe_environment = models.IntegerField(choices=feedback_rating)
    safety_and_security_safety_measures = models.IntegerField(choices=feedback_rating)
    safety_and_security_communication_of_safety_procedures = models.IntegerField(choices=feedback_rating)
    safety_and_security_response_to_safety_concerns = models.IntegerField(choices=feedback_rating)

    service_and_support_friendly_staff = models.IntegerField(choices=feedback_rating)
    service_and_support_support_services_for_students = models.IntegerField(choices=feedback_rating)
    service_and_support_parent_communication = models.IntegerField(choices=feedback_rating)
    service_and_support_appropriate_resources_for_students = models.IntegerField(choices=feedback_rating)

    academic_experience_challenging_program = models.IntegerField(choices=feedback_rating)
    academic_experience_extracurricular_activities = models.IntegerField(choices=feedback_rating)
    academic_experience_effective_communication = models.IntegerField(choices=feedback_rating)

    overall_experience_positive_experience = models.IntegerField(choices=feedback_rating)
    overall_experience_quality_education = models.IntegerField(choices=feedback_rating)
    overall_experience_diversity_and_inclusion = models.IntegerField(choices=feedback_rating)
    overall_experience_recommendation_to_others = models.IntegerField(choices=feedback_rating)

    additional_comments = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['school_experience_student'], name='unique_school_feedback')
        ]