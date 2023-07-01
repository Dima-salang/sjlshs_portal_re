
# Register your models here.
from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields
from import_export.resources import ModelResource
import io
from django.core.files import File
from reportlab.lib.utils import ImageReader
from django.http import FileResponse
from reportlab.pdfgen import canvas
import csv


# Register your models here.


from import_export.admin import ImportExportModelAdmin

"""
The purpose of these classes is to define resources for exporting data from the models
FirstSem_1stQ_11, FirstSem_2ndQ_11, SecondSem_3rdQ_11, and SecondSem_4thQ_11. 
These classes define the fields that will be included in the exported data, 
and specify any pre-processing to be done before exporting. The before_export 
method of each class sets the queryset to None, effectively preventing any data
from being exported. The get_display_name method returns a string that is used 
to identify the resource being exported. This is for security purposes to prevent teachers
from seeing other students' grades.
"""


class FirstSem1stQResource(resources.ModelResource):
    class Meta:
        model = FirstSem_1stQ_11
        exclude = ['id',]
        import_id_fields = ['last_name']
        skip_unchanged = True
        report_skipped = False
        clean_model_instance = True
        fields = ('last_name', 'first_name',
                  'ORALCOMM', 'KOMUNIKASYON', 'GENMATH', 'ELS',
                  'PERDEV', 'LITERATURE', 'PR1', 'SPECIALIZED',
                  'SPECIALIZED_2', 'PE',
                  'AVERAGE', 'lrn')

    def before_export(self, queryset, *args, **kwargs):
        queryset = FirstSem_1stQ_11.objects.none()
        print(queryset)
        return queryset

    def get_display_name(self):
        return 'Custom Grade Resource'


class FirstSem2ndQResource(resources.ModelResource):
    class Meta:
        model = FirstSem_2ndQ_11
        exclude = ['id',]
        import_id_fields = ['last_name']
        skip_unchanged = True
        report_skipped = False
        clean_model_instance = True
        fields = ('last_name', 'first_name',
                  'ORALCOMM', 'KOMUNIKASYON', 'GENMATH', 'ELS',
                  'PERDEV', 'LITERATURE', 'PR1', 'SPECIALIZED',
                  'SPECIALIZED_2', 'PE',
                  'AVERAGE', 'lrn')

    def before_export(self, queryset, *args, **kwargs):
        queryset = FirstSem_2ndQ_11.objects.none()
        print(queryset)
        return queryset

    def get_display_name(self):
        return 'Custom Grade Resource'


class SecondSem3rdQResource(resources.ModelResource):
    class Meta:
        model = SecondSem_3rdQ_11
        exclude = ['id',]
        import_id_fields = ['last_name']
        skip_unchanged = True
        report_skipped = False
        clean_model_instance = True
        fields = ('last_name', 'first_name',
                  'READING_WRITING', 'PAGBASA', 'STATS_PROB', 'PHYSCI',
                  'EMPOWERMENT', 'SPECIALIZED',
                  'SPECIALIZED_2', 'PE2'
                  'AVERAGE', 'lrn')

    def before_export(self, queryset, *args, **kwargs):
        queryset = SecondSem_3rdQ_11.objects.none()
        print(queryset)
        return queryset

    def get_display_name(self):
        return 'Custom Grade Resource'


class SecondSem4thQResource(resources.ModelResource):
    class Meta:
        model = SecondSem_4thQ_11
        exclude = ['id',]
        import_id_fields = ['last_name']
        skip_unchanged = True
        report_skipped = False
        clean_model_instance = True
        fields = ('last_name', 'first_name',
                  'READING_WRITING', 'PAGBASA', 'STATS_PROB', 'PHYSCI',
                  'EMPOWERMENT', 'SPECIALIZED',
                  'SPECIALIZED_2', 'PE2'
                  'AVERAGE', 'lrn')

    def before_export(self, queryset, *args, **kwargs):
        queryset = SecondSem_4thQ_11.objects.none()
        print(queryset)
        return queryset

    def get_display_name(self):
        return 'Custom Grade Resource'


"""
FirstQAdmin, SecondQAdmin, ThirdQAdmin, and FourthQAdmin as Django ModelAdmin subclasses. 
All classes inherit from the ImportExportModelAdmin class. These classes are used to customize
the behavior of Django admin site for specific models.

Each of these classes has two methods defined: get_queryset() and generate_pdf(). 
The get_queryset() method is used to filter the records based on user type. 
If the logged-in user is a superuser, all records are returned. If the user belongs to the 
"Advisors" group, records associated with the adviser are returned. Otherwise, an empty queryset is returned.

The generate_pdf() method is used to generate a PDF report based on the selected records.
It first creates a PDF buffer, and then uses the canvas.
Canvas class from the reportlab library to create a PDF object. 
It then loops through the selected records, adds the data to the PDF, and saves the PDF to the buffer.
Finally, the buffer is returned as a FileResponse with a filename of "grades.pdf".

All classes have an actions attribute that contains a list of actions that can be performed on the selected records. 
In this case, only one action is defined: generate_pdf(). The short_description attribute is used to set the text
that appears in the Django admin site for this action.

All classes have attributes where resource_class is set to a ModelResource which are defined above.
These are classes that define the resources for importing and exporting data to and from the database 
for the associated models.
"""


class FirstQAdmin(ImportExportModelAdmin):
    resource_class = FirstSem1stQResource
    actions = ['generate_pdf']

    list_display = ('lrn','last_name', 'first_name', 'ORALCOMM', 'KOMUNIKASYON', 'GENMATH', 'ELS', 'PERDEV', 'LITERATURE', 'PR1', 'SPECIALIZED', 'SPECIALIZED_2', 'PE', 'Average')
    search_fields = ('last_name', 'first_name', 'lrn')
    list_filter = ('student__section__section', 'student__grade_year')
    ordering = ('last_name', 'first_name')

    fieldsets = (
        (None, {
            'fields': ('last_name', 'first_name', 'lrn')
        }),
        ('Grades', {
            'fields': ('ORALCOMM', 'KOMUNIKASYON', 'GENMATH', 'ELS', 'PERDEV', 'LITERATURE', 'PR1', 'SPECIALIZED', 'SPECIALIZED_2', 'PE', 'Average')
        }),
        ('Student Info', {
            'fields': ('student',),
        }),
    )

    def get_queryset(self, request):

        queryset = super().get_queryset(request)

        if request.user.is_superuser:
            filtered = queryset.select_related('student__section')
            print(f"superuser got queryset {queryset}")
            return filtered
        elif request.user.groups.filter(name="Advisors").exists():
            filtered_queryset = queryset.filter(
                student__section__section_adviser__user_field=request.user).select_related('student__section')
            print(f"advisor got queryset {filtered_queryset}")
            return filtered_queryset
        else:
            print("queryset none")
            return queryset.none()
        
    def get_export_queryset(self, request):
            qs = super().get_export_queryset(request)
            qs = FirstSem_1stQ_11.objects.none()
            return qs

    def generate_pdf(self, request, queryset):
        # create PDF buffer
        buffer = io.BytesIO()

        # create PDF object
        p = canvas.Canvas(buffer)

        # load the layout image
        img_path = f"C:\\Users\\Luis\\PycharmProjects\\SJLSHS_Portal\\SJLSHS_Portal\\sjlshs_backend\\static\\root\\images\\portal-bg.jpg"
        img = ImageReader(img_path)

        # loop through grades and add to PDF
        for grade in queryset:
            print("Grade drawn")
            p.drawImage(img, 0, 0, width=p._pagesize[0], height=p._pagesize[1])
            p.drawString(20, 800, f"Last Name: {grade.last_name}")
            p.drawString(200, 800, f"First Name: {grade.first_name}")
            p.drawString(400, 800, f"LRN: {grade.lrn}")
            p.drawString(20, 700, f"Oral Communication: {grade.ORALCOMM}")
            p.drawString(
                20, 680, f"Komunikasyon at Pananaliksik sa Wika at Kulturang Pilipino: {grade.KOMUNIKASYON}")
            p.drawString(20, 660, f"General Mathematics: {grade.GENMATH}")
            p.drawString(20, 640, f"Earth and Life Science: {grade.ELS}")
            p.drawString(20, 620, f"Personal Development: {grade.PERDEV}")
            p.drawString(20, 600, f"Specialized: {grade.SPECIALIZED}")
            p.drawString(20, 580, f"Specialized: {grade.SPECIALIZED_2}")
            p.drawString(
                20, 560, f"21st Century Literature: {grade.LITERATURE}")
            p.drawString(20, 540, f"Practical Research 1: {grade.PR1}")
            p.drawString(20, 520, f"Physical Education 3: {grade.PE}")
            # add more details to PDF as desired

            p.showPage()

        # save PDF to buffer
        p.save()
        # rewind buffer and create FileResponse
        buffer.seek(0)
        file_name = 'grades.pdf'
        response = FileResponse(buffer, as_attachment=True, filename=file_name)
        return response

    generate_pdf.short_description = "Generate PDF for selected grades"


class SecondQAdmin(ImportExportModelAdmin):
    resource_class = FirstSem2ndQResource
    actions = ['generate_pdf']

    list_display = ('lrn', 'student','last_name', 'first_name', 'ORALCOMM', 'KOMUNIKASYON', 'GENMATH', 'ELS', 'PERDEV', 'LITERATURE', 'PR1', 'SPECIALIZED', 'SPECIALIZED_2', 'PE', 'Average')
    search_fields = ('last_name', 'first_name', 'lrn')
    list_filter = ('student__section__section', 'student__grade_year')
    ordering = ('last_name', 'first_name')

    fieldsets = (
        (None, {
            'fields': ('last_name', 'first_name', 'lrn')
        }),
        ('Grades', {
            'fields': ('ORALCOMM', 'KOMUNIKASYON', 'GENMATH', 'ELS', 'PERDEV', 'LITERATURE', 'PR1', 'SPECIALIZED', 'SPECIALIZED_2', 'PE', 'Average')
        }),
        ('Student Info', {
            'fields': ('student',),
        }),
    )

    def get_queryset(self, request):

        queryset = super().get_queryset(request)

        if request.user.is_superuser:
            filtered = queryset.select_related('student__section')
            print(f"superuser got queryset {queryset}")
            return filtered
        elif request.user.groups.filter(name="Advisors").exists():
            filtered_queryset = queryset.filter(
                student__section__section_adviser__user_field=request.user).select_related('student__section')
            print(f"advisor got queryset {filtered_queryset}")
            return filtered_queryset
        else:
            print("queryset none")
            return queryset.none()
        
    def get_export_queryset(self, request):
            qs = super().get_export_queryset(request)
            qs = FirstSem_2ndQ_11.objects.none()
            return qs

    def generate_pdf(self, request, queryset):
        # create PDF buffer
        buffer = io.BytesIO()

        # create PDF object
        p = canvas.Canvas(buffer)

        # load the layout image
        img_path = f"C:\\Users\\Luis\\PycharmProjects\\SJLSHS_Portal\\SJLSHS_Portal\\sjlshs_backend\\static\\root\\images\\portal-bg.jpg"
        img = ImageReader(img_path)

        # loop through grades and add to PDF
        for grade in queryset:
            print("Grade drawn")
            p.drawImage(img, 0, 0, width=p._pagesize[0], height=p._pagesize[1])
            p.drawString(20, 800, f"Last Name: {grade.last_name}")
            p.drawString(200, 800, f"First Name: {grade.first_name}")
            p.drawString(400, 800, f"LRN: {grade.lrn}")
            p.drawString(20, 700, f"Oral Communication: {grade.ORALCOMM}")
            p.drawString(
                20, 680, f"Komunikasyon at Pananaliksik sa Wika at Kulturang Pilipino: {grade.KOMUNIKASYON}")
            p.drawString(20, 660, f"General Mathematics: {grade.GENMATH}")
            p.drawString(20, 640, f"Earth and Life Science: {grade.ELS}")
            p.drawString(20, 620, f"Personal Development: {grade.PERDEV}")
            p.drawString(20, 600, f"Specialized: {grade.SPECIALIZED}")
            p.drawString(20, 580, f"Specialized: {grade.SPECIALIZED_2}")
            p.drawString(
                20, 560, f"21st Century Literature: {grade.LITERATURE}")
            p.drawString(20, 540, f"Practical Research 1: {grade.PR1}")
            p.drawString(20, 520, f"Physical Education 3: {grade.PE}")
            # add more details to PDF as desired

            p.showPage()

        # save PDF to buffer
        p.save()
        # rewind buffer and create FileResponse
        buffer.seek(0)
        file_name = 'grades.pdf'
        response = FileResponse(buffer, as_attachment=True, filename=file_name)
        return response

    generate_pdf.short_description = "Generate PDF for selected grades"


class ThirdQAdmin(ImportExportModelAdmin):
    resource_class = SecondSem3rdQResource
    actions = ['generate_pdf']

    list_display = ('lrn','last_name', 'first_name', 'READING_WRITING', 'PAGBASA', 'STATS_PROB', 'PHYSCI', 'EMPOWERMENT', 'ENTREP', 'SPECIALIZED', 'SPECIALIZED_2', 'PE2', 'Average')
    search_fields = ('last_name', 'first_name', 'lrn')
    list_filter = ('student__section__section', 'student__grade_year')
    ordering = ('last_name', 'first_name')
    
    fieldsets = (
        (None, {
            'fields': ('last_name', 'first_name', 'lrn')
        }),
        ('Grades', {
            'fields': ('READING_WRITING', 'PAGBASA', 'STATS_PROB', 'PHYSCI', 'EMPOWERMENT', 'ENTREP', 'SPECIALIZED', 'SPECIALIZED_2', 'PE2', 'Average')
        }),
        ('Student Info', {
            'fields': ('student',),
        }),
    )


    def get_queryset(self, request):

        queryset = super().get_queryset(request)

        if request.user.is_superuser:
            filtered = queryset.select_related('student__section')
            print(f"superuser got queryset {queryset}")
            return filtered
        elif request.user.groups.filter(name="Advisors").exists():
            filtered_queryset = queryset.filter(
                student__section__section_adviser__user_field=request.user).select_related('student__section')
            print(f"advisor got queryset {filtered_queryset}")
            return filtered_queryset
        else:
            print("queryset none")
            return queryset.none()
        
    def get_export_queryset(self, request):
            qs = super().get_export_queryset(request)
            qs = SecondSem_3rdQ_11.objects.none()
            return qs

    def generate_pdf(self, request, queryset):
        # create PDF buffer
        buffer = io.BytesIO()

        # create PDF object
        p = canvas.Canvas(buffer)

        # load the layout image
        img_path = f"C:\\Users\\Luis\\PycharmProjects\\SJLSHS_Portal\\SJLSHS_Portal\\sjlshs_backend\\static\\root\\images\\portal-bg.jpg"
        img = ImageReader(img_path)

        # loop through grades and add to PDF
        for grade in queryset:
            print("Grade drawn")
            p.drawImage(img, 0, 0, width=p._pagesize[0], height=p._pagesize[1])
            p.drawString(20, 800, f"Last Name: {grade.last_name}")
            p.drawString(200, 800, f"First Name: {grade.first_name}")
            p.drawString(400, 800, f"LRN: {grade.lrn}")
            p.drawString(
                20, 700, f"Reading and Writing: {grade.READING_WRITING}")
            p.drawString(
                20, 680, f"Pagbasa at Pagsusuri ng Iba't Ibang Teksto Tungo sa Pananaliksik: {grade.PAGBASA}")
            p.drawString(
                20, 660, f"Statistics and Probability: {grade.STATS_PROB}")
            p.drawString(20, 640, f"Physical Science: {grade.PHYSCI}")
            p.drawString(
                20, 620, f"Empowerment Technologies: {grade.EMPOWERMENT}")
            p.drawString(20, 600, f"Specialized: {grade.SPECIALIZED}")
            p.drawString(20, 580, f"Specialized: {grade.SPECIALIZED_2}")
            p.drawString(20, 560, f"Physical Education 3: {grade.PE}")
            # add more details to PDF as desired

            p.showPage()

        # save PDF to buffer
        p.save()
        # rewind buffer and create FileResponse
        buffer.seek(0)
        file_name = 'grades.pdf'
        response = FileResponse(buffer, as_attachment=True, filename=file_name)
        return response

    generate_pdf.short_description = "Generate PDF for selected grades"


class FourthQAdmin(ImportExportModelAdmin):
    resource_class = SecondSem4thQResource
    actions = ['generate_pdf']


    list_display = ('lrn', 'last_name', 'first_name', 'READING_WRITING', 'PAGBASA', 'STATS_PROB', 'PHYSCI', 'EMPOWERMENT', 'ENTREP', 'SPECIALIZED', 'SPECIALIZED_2', 'PE2', 'Average')
    search_fields = ('last_name', 'first_name', 'lrn')
    list_filter = ('student__section__section', 'student__grade_year')
    ordering = ('last_name', 'first_name')
    
    fieldsets = (
        (None, {
            'fields': ('last_name', 'first_name', 'lrn')
        }),
        ('Grades', {
            'fields': ('READING_WRITING', 'PAGBASA', 'STATS_PROB', 'PHYSCI', 'EMPOWERMENT', 'ENTREP', 'SPECIALIZED', 'SPECIALIZED_2', 'PE2', 'Average')
        }),
        ('Student Info', {
            'fields': ('student',),
        }),
    )


    def get_queryset(self, request):

        queryset = super().get_queryset(request)

        if request.user.is_superuser:
            filtered = queryset.select_related('student__section')
            print(f"superuser got queryset {queryset}")
            return filtered
        elif request.user.groups.filter(name="Advisors").exists():
            filtered_queryset = queryset.filter(
                student__section__section_adviser__user_field=request.user).select_related('student__section')
            print(f"advisor got queryset {filtered_queryset}")
            return filtered_queryset
        else:
            print("queryset none")
            return queryset.none()
        

    def get_export_queryset(self, request):
            qs = super().get_export_queryset(request)
            qs = SecondSem_4thQ_11.objects.none()
            return qs

    def generate_pdf(self, request, queryset):
        # create PDF buffer
        buffer = io.BytesIO()

        # create PDF object
        p = canvas.Canvas(buffer)

        # load the layout image
        img_path = f"C:\\Users\\Luis\\PycharmProjects\\SJLSHS_Portal\\SJLSHS_Portal\\sjlshs_backend\\static\\root\\images\\portal-bg.jpg"
        img = ImageReader(img_path)

        # loop through grades and add to PDF
        for grade in queryset:
            print("Grade drawn")
            p.drawImage(img, 0, 0, width=p._pagesize[0], height=p._pagesize[1])
            p.drawString(20, 800, f"Last Name: {grade.last_name}")
            p.drawString(200, 800, f"First Name: {grade.first_name}")
            p.drawString(400, 800, f"LRN: {grade.lrn}")
            p.drawString(
                20, 700, f"Reading and Writing: {grade.READING_WRITING}")
            p.drawString(
                20, 680, f"Pagbasa at Pagsusuri ng Iba't Ibang Teksto Tungo sa Pananaliksik: {grade.PAGBASA}")
            p.drawString(
                20, 660, f"Statistics and Probability: {grade.STATS_PROB}")
            p.drawString(20, 640, f"Physical Science: {grade.PHYSCI}")
            p.drawString(
                20, 620, f"Empowerment Technologies: {grade.EMPOWERMENT}")
            p.drawString(20, 600, f"Specialized: {grade.SPECIALIZED}")
            p.drawString(20, 580, f"Specialized: {grade.SPECIALIZED_2}")
            p.drawString(20, 560, f"Physical Education 3: {grade.PE}")
            # add more details to PDF as desired

            p.showPage()

        # save PDF to buffer
        p.save()
        # rewind buffer and create FileResponse
        buffer.seek(0)
        file_name = 'grades.pdf'
        response = FileResponse(buffer, as_attachment=True, filename=file_name)
        return response

    generate_pdf.short_description = "Generate PDF for selected grades"


admin.site.register(FirstSem_1stQ_11, FirstQAdmin)
admin.site.register(FirstSem_2ndQ_11, SecondQAdmin)
admin.site.register(SecondSem_3rdQ_11, ThirdQAdmin)
admin.site.register(SecondSem_4thQ_11, FourthQAdmin)
