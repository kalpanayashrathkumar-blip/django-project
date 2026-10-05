
from django.contrib import admin
from .models import StudentProfile, Skill , Project , Company , JobRole
from .models import Application ,PlacementRecord

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
@admin.register(PlacementRecord)
class PlacementRecordAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "cgpa",
        "skill_count",
        "project_count",
        "application_count",
        "placement_status",
        "created_at",
    )

    list_filter = ("placement_status",)
    search_fields = ("student__user__username",)