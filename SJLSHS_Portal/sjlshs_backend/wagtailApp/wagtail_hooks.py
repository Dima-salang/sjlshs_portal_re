
from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register)
from .models import StaffMember

class StaffMemberAdmin(ModelAdmin):
    model = StaffMember
    menu_label = 'Staff Members'
    menu_icon = 'user'
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('name', 'title')

modeladmin_register(StaffMemberAdmin)