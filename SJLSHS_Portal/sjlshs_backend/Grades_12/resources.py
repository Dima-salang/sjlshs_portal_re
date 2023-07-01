
from .models import *
from import_export import resources


from import_export import resources, fields, widgets
from .models import StudentGrade, Grade, SpecializedGrade

# class GradeResource(resources.ModelResource):
#     class Meta:
#         model = Grade

# class SpecializedGradeResource(resources.ModelResource):
#     class Meta:
#         model = SpecializedGrade

# class StudentGradeResource(resources.ModelResource):
#     grades = fields.Field(
#         column_name='grades',
#         attribute='grades',
#         widget=widgets.ManyToManyWidget(Grade, field='subject')
#     )
#     specialized_grades = fields.Field(
#         column_name='specialized_grades',
#         attribute='specialized_grades',
#         widget=widgets.ManyToManyWidget(SpecializedGrade, field='subject')
#     )

#     class Meta:
#         model = StudentGrade
#         fields = ('student', 'grades', 'specialized_grades')

