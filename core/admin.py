
from django.contrib import admin
from .models import StudentProfile, Skill , Project , Company , JobRole
from .models import Application

from django.contrib import admin
from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "job",
        "applied_at",
        "status",
    )

    list_filter = (
        "status",
        "applied_at",
    )

    search_fields = (
        "student__user__username",
        "job__title",
        "job__company__name",
    )
admin.site.register(StudentProfile)
admin.site.register(Skill)
admin.site.register(Project)
admin.site.register(Company)
admin.site.register(JobRole)