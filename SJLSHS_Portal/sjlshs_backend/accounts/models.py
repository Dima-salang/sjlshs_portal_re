from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings




# Create your models here.

class TrackAndStrand(models.Model):

    class Meta:
        verbose_name = 'Tracks and Strands'
        verbose_name_plural = 'Tracks and Strands'

    strand = models.CharField(max_length=100)

    def __str__(self):
        return self.strand

class StudentYear(models.Model):
    Grade_Year = models.CharField(max_length=2)


    class Meta:
        verbose_name = 'Grade Level'

    def __str__(self):
        return str(self.Grade_Year)


class StudentSection(models.Model):

    class Meta:
        verbose_name = 'Section'
        verbose_name_plural = 'Sections'

    section_id = models.IntegerField()
    section = models.CharField(max_length=20)
    section_adviser = models.ForeignKey('TeacherUser', null=True,
    on_delete=models.SET_NULL, blank=True)
    room_num = models.SmallIntegerField(blank=True, null=True)

    def __str__(self):
        return self.section

class Subject(models.Model):

    class Meta:
        verbose_name = 'Subject'
        verbose_name_plural = 'Subjects'

    subject_matter = models.CharField(max_length=50)
    grade_year = models.ForeignKey(StudentYear, null=True,
    on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.subject_matter}"
    
class EnrollmentStatus(models.Model):

    class Meta:
        verbose_name = 'Enrollment Status'
        verbose_name_plural = 'Enrollment Statuses'

    enrollment_status = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.enrollment_status}"



class Enrolled_Students(models.Model):

    class Meta:
        verbose_name = 'Enrolled Student'
        verbose_name_plural = 'Enrolled Students'

    lrn = models.CharField(max_length=25, verbose_name="ID Number")
    last_name = models.CharField(max_length=100, verbose_name="Last Name")
    first_name = models.CharField(max_length=100, verbose_name="First Name")
    age = models.PositiveIntegerField(default=0, verbose_name="Age")
    email = models.EmailField(verbose_name="Email Address")
    parent_email = models.EmailField(verbose_name="Parent Email Address", null=True)
    birthday = models.DateField()
    enrollment_status = models.CharField(max_length=50, blank=True, null=True, verbose_name="Enrollment Status")
    grade_year = models.CharField(max_length=2, null=True, blank=True, verbose_name="Grade Year")
    section = models.CharField(max_length=50, null=True,blank=True)
    strand = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.lrn} - {self.last_name}, {self.first_name}"

class StudentUser(AbstractUser):

    """
    Represents a student user in the system, extending the built-in Django
    AbstractUser model. 

    Fields:
    lrn (CharField): the student's Learner Reference Number
    last_name (CharField): the student's last name
    first_name (CharField): the student's first name
    age (PositiveIntegerField): the student's age
    email (EmailField): the student's email address
    birthday (DateField): the student's date of birth
    image_id (ImageField): a proof of enrollment image
    enrollment_status (ForeignKey): the student's enrollment status
    grade_year (ForeignKey): the student's grade year
    section (ForeignKey): the student's section
    strand (ForeignKey): the student's track and strand
    is_email_verified (BooleanField): a flag indicating if the email address 
        has been verified by the user
    data_privacy_agreed (BooleanField): a flag indicating if the user has agreed 
        to the data privacy policy

    Required fields:
    lrn, age, email, birthday
    """

    GRADE_11 = "11"
    GRADE_12 = "12"
    GRADE_YEAR_CHOICES = [
        (GRADE_11, "Grade 11"),
        (GRADE_12, "Grade 12")
    ]

    REGULAR = "Regular"
    IRREGULAR = "Irregular"
    BALIK_ARAL = "Balik-aral"
    ENROLLMENT_STATUS_CHOICES = [
        (REGULAR, "Regular"),
        (IRREGULAR, "Irregular"),
        (BALIK_ARAL, "Balik-Aral")
    ]

    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'


    lrn = models.CharField(max_length=25, verbose_name="ID Number", null=True,)
    last_name = models.CharField(max_length=100, verbose_name="Last Name", null=True)
    first_name = models.CharField(max_length=100, verbose_name="First Name", null=True)
    age = models.PositiveIntegerField(default=0, verbose_name="Age", null=True)
    email = models.EmailField(verbose_name="Email Address", null=True)
    parent_email = models.EmailField(verbose_name="Parent Email Address", null=True)
    birthday = models.DateField(null=True)
    image_id = models.ImageField(upload_to='media/image_id', null=True, verbose_name="Proof of Enrollment")
    enrollment_status = models.CharField(max_length=50, null=True, choices=ENROLLMENT_STATUS_CHOICES, verbose_name="Enrollment Status")
    grade_year = models.CharField(max_length=2, null=True, choices=GRADE_YEAR_CHOICES, verbose_name="Grade Year")
    section = models.ForeignKey(StudentSection, null=True, on_delete=models.SET_NULL, blank=True)
    strand = models.ForeignKey(TrackAndStrand, null=True, on_delete=models.SET_NULL, blank=True)
    is_email_verified = models.BooleanField(null=True, blank=True)
    data_privacy_agreed = models.BooleanField(null=True, verbose_name="I agree to the data privacy policy")
    terms_agreed = models.BooleanField(null=True, verbose_name="I agree to the terms and conditions")

    REQUIRED_FIELDS = ['lrn', 'age', 'email', 'birthday']
                
    def __str__(self):
        return f"{self.lrn} - {self.last_name}, {self.first_name}"
    


class TeacherUser(models.Model):

    """
    Model representing a teacher user.

    Fields:
    - user_field: One-to-one relationship with the StudentUser model.
    - teacher_id: PositiveSmallIntegerField for the teacher's ID.
    - last_name: CharField for the teacher's last name.
    - first_name: CharField for the teacher's first name.
    - email: EmailField for the teacher's email address.
    - contact_num: PositiveBigIntegerField for the teacher's contact number.
    - section_handle: Many-to-many relationship with the StudentSection model.
    - subject_handle: Many-to-many relationship with the Subject model.

    Methods:
    - get_students: Returns a queryset of StudentUser objects associated with the teacher through their sections.

    __str__ method returns the teacher's full name in the format "last_name, first_name".

    """

    class Meta:
        verbose_name = 'Teacher'
        verbose_name_plural = 'Teachers'

    user_field = models.OneToOneField(StudentUser, on_delete=models.CASCADE, blank=True, null=True, related_name='teacheruser')
    teacher_id = models.CharField(max_length=20, null=True)
    last_name = models.CharField(max_length=100, null=True)
    first_name = models.CharField(max_length=100, null=True)
    email = models.EmailField()
    contact_num = models.CharField(max_length=11, null=True)
    advisory_section = models.OneToOneField(StudentSection, on_delete=models.CASCADE, blank=True, null=True, related_name='advisor_section')
    section_handle = models.ManyToManyField(StudentSection, blank=True)
    subject_handle = models.ManyToManyField(Subject, blank=True),
    raw_password = models.CharField(max_length=20, null=True)
    changed_details = models.BooleanField(null=True)

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"
    

    def get_students(self):
        sections = self.section_handle.all()
        if sections:
            return StudentUser.objects.filter(section__in=sections)
        else:
            return StudentUser.objects.none()


class PasswordResetToken(models.Model):
    student = models.OneToOneField(StudentUser, null=True, blank=True, on_delete=models.CASCADE)
    password_token = models.CharField(max_length=50)
    password_token_expiration = models.DateTimeField(null=True, blank=True)
    







