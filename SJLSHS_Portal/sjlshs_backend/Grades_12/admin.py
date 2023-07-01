
from django.contrib import admin
from django.core.paginator import Paginator
from .models import *
from import_export.admin import ImportExportModelAdmin
from import_export import resources
import io
from django.http import FileResponse
from import_export.admin import ImportExportModelAdmin
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image
from reportlab.lib.utils import ImageReader
from django.conf import settings


# Register your models here.


"""
The documentation here is the same for the Grade 11 admin. Refer to that for more information.
"""

class FirstSem1stQResource(resources.ModelResource):
        class Meta:
                model = FirstSem_1stQ
                exclude = ['id',]
                import_id_fields = ['last_name']
                skip_unchanged = True
                report_skipped = False
                clean_model_instance = True
                fields = ('last_name', 'first_name',
                           'PR2', 'CPAR', 'PHILOSOPHY', 'PE',
                             'UCSP', 'EAPP', 'SPECIALIZED',
                               'SPECIALIZED_2',
                                 'AVERAGE', 'lrn')

        

        def get_queryset(self):
                queryset =  super().get_queryset()
                queryset = FirstSem_1stQ.objects.none()
                print(f"Emptied queryset: {queryset}")
                return queryset


        def get_display_name(self):
                return 'Custom Grade Resource'
        
class FirstSem2ndQResource(resources.ModelResource):
        class Meta:
                model = FirstSem_2ndQ
                exclude = ['id',]
                import_id_fields = ['last_name']
                skip_unchanged = True
                report_skipped = False
                clean_model_instance = True
                fields = ('last_name', 'first_name',
                           'PR2', 'CPAR', 'PHILOSOPHY', 'PE',
                             'UCSP', 'EAPP', 'SPECIALIZED',
                               'SPECIALIZED_2',
                                 'AVERAGE', 'lrn')

        

        def before_export(self, queryset, *args, **kwargs):
                queryset = FirstSem_2ndQ.objects.none()
                print(queryset)
                return queryset


        def get_display_name(self):
                return 'Custom Grade Resource'
        
class SecondSem3rdQResource(resources.ModelResource):
        class Meta:
                model = SecondSem_3rdQ
                exclude = ['id',]
                import_id_fields = ['last_name']
                skip_unchanged = True
                report_skipped = False
                clean_model_instance = True
                fields = ('last_name', 'first_name',
                           'PR2', 'CPAR', 'PHILOSOPHY', 'PE4',
                             'UCSP', 'EAPP', 'SPECIALIZED',
                               'SPECIALIZED_2',
                                 'AVERAGE', 'lrn')

        

        def before_export(self, queryset, *args, **kwargs):
                queryset = SecondSem_3rdQ.objects.none()
                print(queryset)
                return queryset


        def get_display_name(self):
                return 'Custom Grade Resource'

class SecondSem4thQResource(resources.ModelResource):
        class Meta:
                model = SecondSem_4thQ
                exclude = ['id',]
                import_id_fields = ['last_name']
                skip_unchanged = True
                report_skipped = False
                clean_model_instance = True
                fields = ('last_name', 'first_name',
                           'PR2', 'CPAR', 'PHILOSOPHY', 'PE4',
                             'UCSP', 'EAPP', 'SPECIALIZED',
                               'SPECIALIZED_2',
                                 'AVERAGE', 'lrn')

        

        def before_export(self, queryset, *args, **kwargs):
                queryset = SecondSem_4thQ.objects.none()
                print(queryset)
                return queryset


        def get_display_name(self):
                return 'Custom Grade Resource'

class FirstQAdmin(ImportExportModelAdmin):
        resource_class = FirstSem1stQResource
        actions = ['generate_pdf']

        list_display = ('lrn', 'last_name', 'first_name', 'PR2', 'CPAR', 'PHILOSOPHY', 'UCSP', 'EAPP', 'SPECIALIZED', 'SPECIALIZED_2', 'PE', 'Average')
        search_fields = ('last_name', 'first_name', 'lrn')
        list_filter = ('student__section__section', 'student__grade_year')
        ordering = ('last_name', 'first_name')
        
        fieldsets = (
                (None, {
                'fields': ('last_name', 'first_name', 'lrn')
                }),
                ('Grades', {
                'fields': ('PR2', 'CPAR', 'PHILOSOPHY', 'UCSP', 'EAPP', 'SPECIALIZED', 'SPECIALIZED_2', 'PE', 'Average')
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
                        filtered_queryset = queryset.filter(student__section__section_adviser__user_field=request.user).select_related('student__section')
                        print(f"advisor got queryset {filtered_queryset}")
                        return filtered_queryset
                else:
                        print("queryset none")
                        return queryset.none()
                
        def get_export_queryset(self, request):
                qs = super().get_export_queryset(request)
                qs = FirstSem_1stQ.objects.none()
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
                        p.drawString(20, 700, f"Practical Research 2: {grade.PR2}")
                        p.drawString(20, 680, f"Contemporary Arts Around the Regions: {grade.CPAR}")
                        p.drawString(20, 660, f"Introduction to the Philosophy of the Human Person: {grade.PHILOSOPHY}")
                        p.drawString(20, 640, f"Understanding Culture, Society, and Politics: {grade.UCSP}")
                        p.drawString(20, 620, f"English for Academic Purposes Program: {grade.EAPP}")
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
class SecondQAdmin(ImportExportModelAdmin):
        resource_class = FirstSem2ndQResource
        actions = ['generate_pdf']

        resource_class = FirstSem1stQResource
        actions = ['generate_pdf']

        list_display = ('lrn','last_name', 'first_name', 'PR2', 'CPAR', 'PHILOSOPHY', 'UCSP', 'EAPP', 'SPECIALIZED', 'SPECIALIZED_2', 'PE', 'Average')
        search_fields = ('last_name', 'first_name', 'lrn')
        list_filter = ('student__section__section', 'student__grade_year')
        ordering = ('last_name', 'first_name')
        
        fieldsets = (
                (None, {
                'fields': ('last_name', 'first_name', 'lrn')
                }),
                ('Grades', {
                'fields': ('PR2', 'CPAR', 'PHILOSOPHY', 'UCSP', 'EAPP', 'SPECIALIZED', 'SPECIALIZED_2', 'PE', 'Average')
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
                        filtered_queryset = queryset.filter(student__section__section_adviser__user_field=request.user).select_related('student__section')
                        print(f"advisor got queryset {filtered_queryset}")
                        return filtered_queryset
                else:
                        print("queryset none")
                        return queryset.none()
                

        def get_export_queryset(self, request):
                qs = super().get_export_queryset(request)
                qs = FirstSem_2ndQ.objects.none()
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
                        p.drawString(20, 700, f"Practical Research 2: {grade.PR2}")
                        p.drawString(20, 680, f"Contemporary Arts Around the Regions: {grade.CPAR}")
                        p.drawString(20, 660, f"Introduction to the Philosophy of the Human Person: {grade.PHILOSOPHY}")
                        p.drawString(20, 640, f"Understanding Culture, Society, and Politics: {grade.UCSP}")
                        p.drawString(20, 620, f"English for Academic Purposes Program: {grade.EAPP}")
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
        
        
class ThirdQAdmin(ImportExportModelAdmin):
        resource_class = SecondSem3rdQResource
        actions = ['generate_pdf']

        list_display = ('lrn','last_name', 'first_name', 'III', 'MIL', 'PE4', 'IMMERSION', 'SPECIALIZED', 'SPECIALIZED_2', 'Average')
        search_fields = ('last_name', 'first_name', 'lrn')
        list_filter = ('student__section__section', 'student__grade_year')
        ordering = ('last_name', 'first_name')

        fieldsets = (
                (None, {
                'fields': ('last_name', 'first_name', 'lrn')
                }),
                ('Grades', {
                'fields': ('III', 'MIL', 'PE4', 'IMMERSION', 'SPECIALIZED', 'SPECIALIZED_2', 'Average')
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
                        filtered_queryset = queryset.filter(student__section__section_adviser__user_field=request.user).select_related('student__section')
                        print(f"advisor got queryset {filtered_queryset}")
                        return filtered_queryset
                else:
                        print("queryset none")
                        return queryset.none()
                
        def get_export_queryset(self, request):
                qs = super().get_export_queryset(request)
                qs = SecondSem_3rdQ.objects.none()
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
                        p.drawString(20, 700, f"Inquiries, Investigations, Immersion: {grade.III}")
                        p.drawString(20, 680, f"Media and Information Literacy: {grade.MIL}")
                        p.drawString(20, 660, f"Physical Education and Health 4: {grade.PE4}")
                        p.drawString(20, 640, f"Work Immersion: {grade.IMMERSION}")
                        p.drawString(20, 600, f"Specialized: {grade.SPECIALIZED}")
                        p.drawString(20, 580, f"Specialized: {grade.SPECIALIZED_2}")
                        
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

        list_display = ('lrn','last_name', 'first_name', 'III', 'MIL', 'PE4', 'IMMERSION', 'SPECIALIZED', 'SPECIALIZED_2', 'Average')
        search_fields = ('last_name', 'first_name', 'lrn')
        list_filter = ('student__section__section', 'student__grade_year')
        ordering = ('last_name', 'first_name')

        fieldsets = (
                (None, {
                'fields': ('last_name', 'first_name', 'lrn')
                }),
                ('Grades', {
                'fields': ('III', 'MIL', 'PE4', 'IMMERSION', 'SPECIALIZED', 'SPECIALIZED_2', 'Average')
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
                        filtered_queryset = queryset.filter(student__section__section_adviser__user_field=request.user).select_related('student__section')
                        print(f"advisor got queryset {filtered_queryset}")
                        return filtered_queryset
                else:
                        print("queryset none")
                        return queryset.none()
                
        def get_export_queryset(self, request):
                qs = super().get_export_queryset(request)
                qs = SecondSem_4thQ.objects.none()
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
                        p.drawString(20, 700, f"Inquiries, Investigations, Immersion: {grade.III}")
                        p.drawString(20, 680, f"Media and Information Literacy: {grade.MIL}")
                        p.drawString(20, 660, f"Physical Education and Health 4: {grade.PE4}")
                        p.drawString(20, 640, f"Work Immersion: {grade.IMMERSION}")
                        p.drawString(20, 600, f"Specialized: {grade.SPECIALIZED}")
                        p.drawString(20, 580, f"Specialized: {grade.SPECIALIZED_2}")
                        
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
        

admin.site.register(FirstSem_1stQ, FirstQAdmin)
admin.site.register(FirstSem_2ndQ, SecondQAdmin)
admin.site.register(SecondSem_3rdQ, ThirdQAdmin)
admin.site.register(SecondSem_4thQ, FourthQAdmin)

