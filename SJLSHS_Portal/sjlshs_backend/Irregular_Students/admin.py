from django.contrib import admin
from .models import IrregularStudent, SubjectGrade
# Register your models here.
from django.forms import BaseInlineFormSet
from django.forms.models import inlineformset_factory


"""
This module defines the admin interface for IrregularStudent model and SubjectGrade model.
It registers the models with the Django admin site, and provides customization for the
SubjectGradeInline formset.

Classes:
- SubjectGradeInlineFormSet: A custom inline formset for the SubjectGrade model.
- SubjectGradeInline: A TabularInline for the SubjectGrade model.
- IrregularStudentAdmin: A ModelAdmin for the IrregularStudent model.

Functions:
- get_queryset: A method of IrregularStudentAdmin that filters the queryset based on the user's role.

"""

class SubjectGradeInlineFormSet(BaseInlineFormSet):
    
    """
    A custom inline formset for the SubjectGrade model that selects related objects.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queryset = self.queryset.select_related('subject')

class SubjectGradeInline(admin.StackedInline):
    
    """
    A TabularInline for the SubjectGrade model that uses the custom formset.
    """

    model = SubjectGrade
    formset = SubjectGradeInlineFormSet
    extra = 8

class IrregularStudentAdmin(admin.ModelAdmin):
    
    """
    A ModelAdmin for the IrregularStudent model that defines custom behavior for the queryset based on the user's role.
    """

    inlines = [SubjectGradeInline]

    list_display = ('student', 'academic_period', 'name')
    list_filter = ('academic_period',)
    search_fields = ('name', 'student__first_name', 'student__last_name')

    def get_queryset(self, request):

                queryset = super().get_queryset(request)
                
                if request.user.is_superuser:
                        filtered = queryset.select_related('student__section')
                        print(f"superuser got queryset {queryset}")
                        return filtered
                elif request.user.groups.filter(name="Advisors").exists():
                        filtered_queryset = queryset.filter(student__section__section_adviser__user_field=request.user).select_related('student__section')
                        print(f"advisor got queryset {filtered_queryset}")
                        return filtered_queryset
                else:
                        print("queryset none")
                        return queryset.none()

class SubjectGradeAdmin(admin.ModelAdmin):
       list_display = ['student', 'subject', 'grade']
       list_filter = ['subject']
       search_fields = ['student__name']
    

admin.site.register(IrregularStudent, IrregularStudentAdmin)    
admin.site.register(SubjectGrade, SubjectGradeAdmin)
