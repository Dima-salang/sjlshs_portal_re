from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin
from .forms import CustomCreationForm, CustomerUserChangeForm, UserCreationForm
from .models import *
from Grades_12.models import *
from std_portal.models import *
from django.contrib.auth.models import Group
from std_portal.admin import PostAdmin
from django.urls import reverse
from django.shortcuts import redirect
from django.db.models import Q


class TeacherAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'email', 'contact_num', 'teacher_id')
    search_fields = ('last_name', 'first_name', 'email', 'teacher_id')

    actions = ['ger_raw_password']

    
    def get_raw_password(self, request, queryset):
        if request.user.is_superuser:
            for teacher in queryset:
                self.message_user(request, f"{teacher.username} - Raw Password: {teacher.raw_password}")
        else:
            self.message_user(request, "You do not have the appropriate access to this.")
    get_raw_password.short_description = "Get the raw password for the teacher for account creation"

    
class TeacherAdminArea(admin.AdminSite):
    """TeacherAdminArea: 
    A custom admin site class that inherits from the built-in `admin.AdminSite` class.
    It sets the `site_header` attribute to "Teachers' Administration Site"."""

    site_header = "Teachers' Administration Site"


class StudentUserAdmin(admin.ModelAdmin):

    """
    StudentUserAdmin:
        A custom ModelAdmin class for the `StudentUser` model.
        It overrides the `get_queryset` method to filter the queryset based on the requesting user's permissions:
            - If the requesting user is a superuser, the method returns the original queryset with related `TeacherUser` instances pre-fetched using `select_related()`.
            - If the requesting user belongs to the "Teacher" group, the method returns a filtered queryset of the requesting teacher's students with their related `TeacherUser` instances pre-fetched.
            - Otherwise, the method returns an empty queryset.
        The `fields` attribute is a modified version of the `UserAdmin` fieldsets, with the first fieldset's title set to `None` and the field names reordered.

    Fields:
        A list of tuples representing the fieldsets for the default `UserAdmin` class.
        The first tuple's title is set to `None`, and the fields are reordered.
    """
    actions = ['promote_and_delete_accounts', "verify_student_registration"]

    #customize admin view

    list_display = ('lrn', 'last_name', 'first_name', 'email', 'enrollment_status', 'grade_year')
    list_filter = ('last_name', 'enrollment_status', 'grade_year')
    ordering = ('-date_joined',)
    search_fields = ('lrn', 'last_name', 'first_name', 'email')

    model = StudentUser


    # filter the queryset
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset.select_related('teacheruser')
        elif request.user.groups.filter(Q(name="Teacher") | Q(name="Advisors")).exists():
            return request.user.teacheruser.get_students().select_related('teacheruser')
        else:
            return queryset.none()
        

    """Command for promoting grade 11 students and deleting grade 12 accounts"""

    def promote_and_delete_accounts(self, request, queryset):
        if not request.user.is_superuser:
            self.message_user(request, message="You do not have permission to execute this command.")
            return

        grade_11_year = StudentYear.objects.get(Grade_Year="11")
        grade_12_year = StudentYear.objects.get(Grade_Year="12")

        # Delete graduating accounts
        users_to_delete = StudentUser.objects.filter(grade_year=grade_12_year)
        self.message_user(request, f"Found {users_to_delete.count()} users to delete")
        for user in users_to_delete:
            user.delete()
            self.message_user(request, f"Deleted {user.last_name}, {user.first_name}")

        
        # Promote students
        StudentUser.objects.filter(grade_year=grade_11_year).update(grade_year=grade_12_year)

        self.message_user(request, "Success! Promoted students!")
        return redirect(reverse('admin:yourapp_studentuser_changelist'))
    
    promote_and_delete_accounts.short_description = "Promote Grade 11 students and delete graduating accounts"

    def verify_student_registration(self, request, queryset):
        if not request.user.is_superuser:
            self.message_user(request, message="You do not have permission to execute this command.")
            return

        for student_user in queryset:
            try:
                enrolled_student = Enrolled_Students.objects.get(lrn=student_user.lrn)
                matched_fields = []

                if enrolled_student.last_name == student_user.last_name:
                    matched_fields.append('Last Name')
                if enrolled_student.first_name == student_user.first_name:
                    matched_fields.append('First Name')
                if enrolled_student.email == student_user.email:
                    matched_fields.append('Email')
                if enrolled_student.parent_email == student_user.parent_email:
                    matched_fields.append('Parent Email')
                if enrolled_student.birthday == student_user.birthday:
                    matched_fields.append('Birthday')
                if enrolled_student.grade_year == student_user.grade_year:
                    matched_fields.append('Grade Year')
                if enrolled_student.enrollment_status == student_user.enrollment_status:
                    matched_fields.append('Enrollment Status')

                if matched_fields:
                    message = f"""The following fields have matched for LRN {student_user.lrn} - {student_user.last_name}, {student_user.first_name}: {matched_fields}.
                    Found the following match:
                    New User:                       Enrolled Student:
                    {student_user.lrn}              {enrolled_student.lrn}
                    {student_user.last_name}        {enrolled_student.last_name}
                    {student_user.first_name}       {enrolled_student.first_name}
                    {student_user.email}            {enrolled_student.email}
                    {student_user.parent_email}     {enrolled_student.parent_email}
                    {student_user.birthday}         {enrolled_student.birthday}
                    {student_user.grade_year}       {enrolled_student.grade_year}
                    {student_user.enrollment_status}{enrolled_student.enrollment_status}"""
                else:
                    message = f"No fields matched for LRN {student_user.lrn}"
                
                self.message_user(request, message, level=messages.INFO)
            except Enrolled_Students.DoesNotExist:
                message = f"No enrolled student was found with LRN {student_user.lrn}"
                self.message_user(request, message, level=messages.ERROR)

    verify_student_registration.short_description = "Verify student registration"


fields = list(UserAdmin.fieldsets)
fields[0] = (None, {'fields': ('lrn', 'username', 'password', 'birthday', 'section', 'grade_year', 'strand')})

"""
admin.site.site_header:
    A string representing the site header for the default admin site (accessible at `/admin/`).
    It's set to "SJLSHS Portal".
"""
admin.site.site_header = "SJLSHS Portal"



class CustomAdmin(UserAdmin):
    """
    Defines a custom admin class for the `StudentUser` model, based on the built-in `UserAdmin` class.

    CustomAdmin:
        A custom admin class that extends the `UserAdmin` class and sets the following attributes:
            - `add_form`: A form class used for adding new `StudentUser` instances.
            - `form`: A form class used for editing `StudentUser` instances.
            - `list_display`: A list of field names to display in the admin's list view for `StudentUser` instances.
            - `model`: The `StudentUser` model this admin class is associated with.
            - `add_fieldsets`: A tuple representing the fieldsets for the add view of `StudentUser` instances.

    Fields:
        A list of tuples representing the fieldsets for the default `UserAdmin` class.

    CustomAdmin.fieldsets:
        A tuple representing the fieldsets for the `CustomAdmin` class. It's set to `fields`.
    """
    add_form = CustomCreationForm
    form = CustomerUserChangeForm
    list_display = ['lrn', 'last_name', 'first_name', 'section', 'birthday', 'username', 'email', 'strand']
    model = StudentUser
    add_fieldsets = tuple(fields)

CustomAdmin.fieldsets = tuple(fields)

# registering models to admin site 
admin.site.register(StudentUser, StudentUserAdmin)
admin.site.register(TeacherUser, TeacherAdmin)
admin.site.register(StudentSection)
admin.site.register(StudentYear)
admin.site.register(Subject)
admin.site.register(Enrolled_Students)
admin.site.register(TrackAndStrand)
admin.site.register(EnrollmentStatus)
admin.site.register(PasswordResetToken)





teacher_site = TeacherAdminArea(name="TeacherAdminSite")
teacher_site.register(StudentUser, StudentUserAdmin)
teacher_site.register(Post, PostAdmin)
teacher_site.register(Schedule)



