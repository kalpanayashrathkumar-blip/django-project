from rest_framework import serializers
from .models import StudentProfile , Company , JobRole ,Application



class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = [
            "id",
            "phone",
            "college",
            "branch",
            "graduation_year",
            "cgpa",
            "skills",
            "profile_photo",
            "resume",
        ]
class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = [
            "id",
            "name",
        ]   
class JobRoleSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(
        source="company.name",
        read_only=True
    )

    required_skills = serializers.StringRelatedField(
        many=True,
        read_only=True
    )

    class Meta:
        model = JobRole
        fields = [
            "id",
            "title",
            "company",
            "company_name",
            "minimum_cgpa",
            "required_skills",
        ]   
class ApplicationSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(
        source="job.title",
        read_only=True
    )

    company_name = serializers.CharField(
        source="job.company.name",
        read_only=True
    )

    class Meta:
        model = Application
        fields = [
            "id",
            "student",
            "job",
            "job_title",
            "company_name",
            "applied_at",
            "status",
        ]                  