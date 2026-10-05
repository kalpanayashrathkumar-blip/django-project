from django.db import models
from django.contrib.auth.models import User


class Skill(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.name 
class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    phone = models.CharField(max_length=15)
    college = models.CharField(max_length=200)
    branch = models.CharField(max_length=100)
    graduation_year = models.IntegerField()
    cgpa = models.DecimalField(max_digits=4, decimal_places=2)
    
    profile_photo = models.ImageField(
    upload_to="profile_photos/",
    blank=True,
    null=True
   
    )
    resume = models.FileField(
    upload_to="resumes/",
    blank=True,
    null=True
)

    skills = models.ManyToManyField(Skill, blank=True)


    def __str__(self):
        return self.user.username
class Project(models.Model):
    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name="projects"
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    technologies = models.CharField(max_length=300)
    github_link = models.URLField(blank=True)
    
    def __str__(self):
        return self.title
class Company(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return self.name


class JobRole(models.Model):
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="job_roles"
    )
    title = models.CharField(max_length=200)
    minimum_cgpa = models.DecimalField(
        max_digits=4,
        decimal_places=2
    )
    required_skills = models.ManyToManyField(
        Skill,
        blank=True
    )

    def __str__(self):
        return f"{self.company.name} - {self.title}" 
class Application(models.Model):
    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE
    )

    job = models.ForeignKey(
        JobRole,
        on_delete=models.CASCADE
    )

    applied_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=20,
        default="Applied"
    )

    def __str__(self):
        return f"{self.student.user.username} - {self.job.title}"    
class PlacementRecord(models.Model):
    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE
    )
    cgpa = models.FloatField()
    skill_count = models.IntegerField(default=0)
    project_count = models.IntegerField(default=0)
    application_count = models.IntegerField(default=0)

    placement_status = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.user.username} - {self.placement_status}" 
    