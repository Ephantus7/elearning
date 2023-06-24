from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from embed_video.admin import AdminVideoMixin
from django.urls import reverse_lazy


class AuxilliaryAdminSite(admin.AdminSite):
    site_header = "E-Learning Platform Content Management Portal"
    site_title = "E-Learning Platform Content Management Portal"
    site_url = reverse_lazy('dashboard')
    index_title = "Welcome to Elearning Platform Content Management Portal"
    login_template = "registration/login.html"


auxilliary_admin_site = AuxilliaryAdminSite(name="aux_admin")


class VideoAdmin(AdminVideoMixin, admin.ModelAdmin):
    pass


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'username', 'user_type']

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('user_type', 'profile_pic')}),
    )


class FilterModelAdmin(admin.ModelAdmin):
    list_filter = [
        ("subject", admin.RelatedOnlyFieldListFilter)
    ]


# custom admin site header
admin.site.site_header = 'Elearning Platform | Main Admin'
admin.site.site_title = 'Main Admin | Elearning Platform'
admin.site.index_title = 'Admin | Elearning Platform'

admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Course)
admin.site.register(Subject)
admin.site.register(Book)
admin.site.register(Video, VideoAdmin)
admin.site.register(PastPaper)
admin.site.register(Assignment)
admin.site.register(AssignmentUploads)
admin.site.register(AssignmentScores)
admin.site.register(AssignmentCategory)

auxilliary_admin_site.register(Book, FilterModelAdmin)
auxilliary_admin_site.register(Video, VideoAdmin)
auxilliary_admin_site.register(PastPaper, FilterModelAdmin)
auxilliary_admin_site.register(Assignment, FilterModelAdmin)
