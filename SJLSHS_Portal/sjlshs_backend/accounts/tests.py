from django.test import TestCase
from .models import TrackAndStrand, StudentYear, StudentSection, Subject, EnrollmentStatus, StudentUser, TeacherUser
from datetime import date
from django.core.files.uploadedfile import SimpleUploadedFile

class TrackAndStrandModelTestCase(TestCase):
    def setUp(self):
        self.track_and_strand = TrackAndStrand.objects.create(strand="Science")


    def test_strand_max_length(self):
        max_length = self.track_and_strand._meta.get_field('strand').max_length
        self.assertEquals(max_length, 100)

    def test_strand_str(self):
        expected_strand_name = f'{self.track_and_strand.strand}'
        self.assertEquals(expected_strand_name, str(self.track_and_strand))

    def test_strand_label(self):
        field_label = self.track_and_strand._meta.get_field('strand').verbose_name
        self.assertEquals(field_label, 'strand')


class StudentYearModelTest(TestCase):

    def setUp(self):
        StudentYear.objects.create(Grade_Year='10')
        StudentYear.objects.create(Grade_Year='11')
        StudentYear.objects.create(Grade_Year='12')

    def test_grade_year_label(self):
        student_year = StudentYear.objects.get(Grade_Year='10')
        field_label = student_year._meta.get_field('Grade_Year').verbose_name
        self.assertEqual(field_label, 'Grade Year')

    def test_grade_year_max_length(self):
        student_year = StudentYear.objects.get(Grade_Year='11')
        max_length = student_year._meta.get_field('Grade_Year').max_length
        self.assertEqual(max_length, 2)

    def test_grade_year_str(self):
        student_year = StudentYear.objects.get(Grade_Year='12')
        self.assertEqual(str(student_year), '12')


class StudentSectionModelTestCase(TestCase):
    def setUp(self):
        self.section = StudentSection.objects.create(section_id=1, section="Section A", room_num=101)

    def test_section_id_label(self):
        field_label = self.section._meta.get_field('section_id').verbose_name
        self.assertEqual(field_label, 'section id')

    def test_section_label(self):
        field_label = self.section._meta.get_field('section').verbose_name
        self.assertEqual(field_label, 'section')

    def test_section_adviser_label(self):
        field_label = self.section._meta.get_field('section_adviser').verbose_name
        self.assertEqual(field_label, 'section adviser')

    def test_room_num_label(self):
        field_label = self.section._meta.get_field('room_num').verbose_name
        self.assertEqual(field_label, 'room num')

    def test_section_str(self):
        self.assertEqual(str(self.section), 'Section A')
    
    def test_section_adviser_null(self):
        self.assertEqual(self.section.section_adviser, None)
    
    def test_room_num_null(self):
        self.assertEqual(self.section.room_num, 101)
    
    def test_section_id_is_positive(self):
        self.assertGreaterEqual(self.section.section_id, 0)


class SubjectModelTestCase(TestCase):
    
    def setUp(self):
        self.year_1 = StudentYear.objects.create(Grade_Year='1')
        self.year_2 = StudentYear.objects.create(Grade_Year='2')
        self.subject_1 = Subject.objects.create(subject_matter='Math', grade_year=self.year_1)
        self.subject_2 = Subject.objects.create(subject_matter='Science', grade_year=self.year_2)
    
    def test_subject_str(self):
        self.assertEqual(str(self.subject_1), 'Math - 1')
        self.assertEqual(str(self.subject_2), 'Science - 2')
    
    def test_subject_grade_year(self):
        self.assertEqual(self.subject_1.grade_year, self.year_1)
        self.assertEqual(self.subject_2.grade_year, self.year_2)


class EnrollmentStatusTestCase(TestCase):
    def setUp(self):
        EnrollmentStatus.objects.create(enrollment_status='Enrolled')
        EnrollmentStatus.objects.create(enrollment_status='Dropped')

    def test_enrollment_status_str(self):
        enrolled = EnrollmentStatus.objects.get(enrollment_status='Enrolled')
        dropped = EnrollmentStatus.objects.get(enrollment_status='Dropped')
        self.assertEqual(str(enrolled), 'Enrolled')
        self.assertEqual(str(dropped), 'Dropped')


class StudentUserModelTestCase(TestCase):

    def setUp(self):
        self.enrollment_status = EnrollmentStatus.objects.create(enrollment_status='Enrolled')
        self.grade_year = StudentYear.objects.create(Grade_Year='12')
        self.section = StudentSection.objects.create(section_id=1, section='Section A')
        self.strand = TrackAndStrand.objects.create(strand='STEM')
        self.student_data = {
            'lrn': '123456789012345',
            'last_name': 'Doe',
            'first_name': 'John',
            'age': 18,
            'email': 'johndoe@example.com',
            'birthday': date(2004, 4, 17),
            'enrollment_status': self.enrollment_status,
            'grade_year': self.grade_year,
            'section': self.section,
            'strand': self.strand,
            'is_email_verified': True,
            'data_privacy_agreed': True
        }

    def test_create_student_user(self):
        student = StudentUser.objects.create(**self.student_data)
        self.assertEqual(student.lrn, self.student_data['lrn'])
        self.assertEqual(student.last_name, self.student_data['last_name'])
        self.assertEqual(student.first_name, self.student_data['first_name'])
        self.assertEqual(student.age, self.student_data['age'])
        self.assertEqual(student.email, self.student_data['email'])
        self.assertEqual(student.birthday, self.student_data['birthday'])
        self.assertEqual(student.enrollment_status, self.enrollment_status)
        self.assertEqual(student.grade_year, self.grade_year)
        self.assertEqual(student.section, self.section)
        self.assertEqual(student.strand, self.strand)
        self.assertTrue(student.is_email_verified)
        self.assertTrue(student.data_privacy_agreed)

    def test_required_fields(self):
        student_data = self.student_data.copy()
        for field in StudentUser.REQUIRED_FIELDS:
            student_data.pop(field)
            with self.assertRaises(Exception) as context:
                student = StudentUser.objects.create(**student_data)
                self.assertTrue(field in str(context.exception))

    def test_string_representation(self):
        student = StudentUser.objects.create(**self.student_data)
        expected = f"{self.student_data['lrn']} - {self.student_data['last_name']}, {self.student_data['first_name']} ({self.section})"
        self.assertEqual(str(student), expected)

    def test_image_upload(self):
        image_file = SimpleUploadedFile('test_image.jpg', b'test content')
        self.student_data['image_id'] = image_file
        student = StudentUser.objects.create(**self.student_data)
        self.assertTrue(student.image_id.name.endswith('.jpg'))
        self.assertEqual(student.image_id.read(), b'test content')

    def test_blank_and_null_fields(self):
        self.student_data['enrollment_status'] = None
        self.student_data['section'] = None
        self.student_data['strand'] = None
        self.student_data['is_email_verified'] = None
        self.student_data['data_privacy_agreed'] = None
        student = StudentUser.objects.create(**self.student_data)
        self.assertIsNone(student.enrollment_status)
        self.assertIsNone(student.section)
        self.assertIsNone(student.strand)
        self.assertIsNone(student.is_email_verified)
        self.assertIsNone(student.data_privacy_agreed)

class TeacherUserTestCase(TestCase):

    def setUp(self):
        self.section1 = StudentSection.objects.create(section_id=1, section='Section A')
        self.section2 = StudentSection.objects.create(section_id=2, section='Section B')
        self.subject1 = Subject.objects.create(subject_matter='Math', grade_year=None)
        self.subject2 = Subject.objects.create(subject_matter='Science', grade_year=None)
        self.teacher = TeacherUser.objects.create(
            teacher_id=1,
            last_name='Doe',
            first_name='John',
            email='johndoe@example.com',
            contact_num=1234567890
        )

    def test_teacher_string_representation(self):
        self.assertEqual(str(self.teacher), 'Doe, John')

    def test_get_students_with_sections(self):
        # Add section1 and section2 to teacher's section_handle
        self.teacher.section_handle.add(self.section1, self.section2)

        # Create student1 and student2 with section1, and student3 with section2
        student1 = StudentUser.objects.create(lrn='111', last_name='Doe', first_name='Jane', age=18, email='janedoe@example.com', birthday='2005-01-01', section=self.section1)
        student2 = StudentUser.objects.create(username="luis", lrn='222', last_name='Smith', first_name='John', age=17, email='johnsmith@example.com', birthday='2006-01-01', section=self.section1)
        student3 = StudentUser.objects.create(username="gabrielle", lrn='333', last_name='Brown', first_name='Mary', age=16, email='marybrown@example.com', birthday='2007-01-01', section=self.section2)

        # Check if get_students returns the correct queryset
        students = self.teacher.get_students()
        self.assertEqual(students.count(), 3)
        self.assertIn(student1, students)
        self.assertIn(student2, students)
        self.assertIn(student3, students)

    def test_get_students_without_sections(self):
        # Check if get_students returns none when teacher has no sections
        students = self.teacher.get_students()
        self.assertEqual(students.count(), 0)

    def test_add_subjects(self):
        # Add subject1 and subject2 to teacher's subject_handle
        self.teacher.subject_handle.add(self.subject1, self.subject2)

        # Check if teacher has both subjects
        subjects = self.teacher.subject_handle.all()
        self.assertEqual(subjects.count(), 2)
        self.assertIn(self.subject1, subjects)
        self.assertIn(self.subject2, subjects)

    def test_remove_subjects(self):
        # Add subject1 and subject2 to teacher's subject_handle
        self.teacher.subject_handle.add(self.subject1, self.subject2)

        # Remove subject1 from teacher's subject_handle
        self.teacher.subject_handle.remove(self.subject1)

        # Check if teacher has only subject2
        subjects = self.teacher.subject_handle.all()
        self.assertEqual(subjects.count(), 1)
        self.assertNotIn(self.subject1, subjects)
        self.assertIn(self.subject2, subjects)
