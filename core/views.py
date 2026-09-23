from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from .models import Application
from .models import StudentProfile, JobRole ,Project ,Company
from .services import check_eligibility, get_dashboard_data,   get_profile_completion, get_skill_gap,  get_skill_recommendations
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.models import User
from .forms import RegistrationForm ,StudentProfileForm , ProjectForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import user_passes_test

from django.shortcuts import render, get_object_or_404, redirect

def check_job_eligibility(request, job_id):
    student = get_object_or_404(
        StudentProfile,
        user=request.user
    )

    job_role = get_object_or_404(
        JobRole,
        id=job_id
    )

    result = check_eligibility(student, job_role)

    context = {
        "job_role": job_role,
        "result": result,
    }

    return render(
        request,
        "core/eligibility.html",
        context
    )
def job_list(request):
    job_roles = JobRole.objects.select_related("company").prefetch_related(
        "required_skills"
    )

    return render(
        request,
        "core/job_list.html",
        {"job_roles": job_roles}
    )

@login_required
def dashboard(request):
    student = get_object_or_404(
        StudentProfile.objects.prefetch_related(
            "skills",
            "projects"
        ),
        user=request.user
    )

    dashboard_data = get_dashboard_data(student)
    profile_completion = get_profile_completion(student)
    skill_gap = get_skill_gap(student)
    skill_recommendations = get_skill_recommendations(skill_gap)
    applications = Application.objects.filter(
    student=student
)

    total_applications = applications.count()

    shortlisted = applications.filter(
    status="Shortlisted"
    ).count()

    selected = applications.filter(
    status="Selected"
    ).count()

    rejected = applications.filter(
    status="Rejected"
    ).count()
    return render(
        request,
        "core/dashboard.html",
        {
            "student": student,
            "dashboard_data": dashboard_data,
            "profile_completion": profile_completion,
            "skill_gap": skill_gap,
            "recommendations": skill_recommendations,
            "total_applications": total_applications,
            "shortlisted": shortlisted,
            "selected": selected,
            "rejected": rejected,
        }
    )
def register(request):

    if request.method == "POST":

        form = RegistrationForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            user.set_password(
                form.cleaned_data["password"]
            )

            user.save()

            login(request, user)

            return redirect("create_profile")

    else:
        form = RegistrationForm()

    return render(
        request,
        "core/register.html",
        {"form": form}
    )
def create_profile(request):

    if hasattr(request.user, "studentprofile"):
        return redirect("dashboard")

    if request.method == "POST":

        form = StudentProfileForm(request.POST)

        if form.is_valid():

            profile = form.save(commit=False)

            profile.user = request.user

            profile.save()

            return redirect("dashboard")

    else:
        form = StudentProfileForm()

    return render(
        request,
        "core/create_profile.html",
        {"form": form}
    )
def add_project(request):

    student = get_object_or_404(
        StudentProfile,
        user=request.user
    )

    if request.method == "POST":

        form = ProjectForm(request.POST)

        if form.is_valid():

            project = form.save(commit=False)

            project.student = student

            project.save()

            return redirect("dashboard")

    else:
        form = ProjectForm()

    return render(
        request,
        "core/add_project.html",
        {"form": form}
    )
def delete_project(request, project_id):

    student = get_object_or_404(
        StudentProfile,
        user=request.user
    )

    project = get_object_or_404(
        Project,
        id=project_id,
        student=student
    )

    if request.method == "POST":
        project.delete()
        return redirect("dashboard")

    return render(
        request,
        "core/delete_project.html",
        {"project": project}
    )
def edit_project(request, project_id):

    student = get_object_or_404(
        StudentProfile,
        user=request.user
    )

    project = get_object_or_404(
        Project,
        id=project_id,
        student=student
    )

    if request.method == "POST":

        form = ProjectForm(
            request.POST,
            instance=project
        )

        if form.is_valid():
            form.save()
            return redirect("dashboard")

    else:
        form = ProjectForm(instance=project)

    return render(
        request,
        "core/edit_project.html",
        {"form": form, "project": project}
    )
def edit_profile(request):

    student = get_object_or_404(
        StudentProfile,
        user=request.user
    )

    if request.method == "POST":

        form = StudentProfileForm(
            request.POST or None,
            request.FILES or None,
            instance=student
        )

        if form.is_valid():
            form.save()
            return redirect("dashboard")

    else:
        form = StudentProfileForm(instance=student)

    return render(
        request,
        "core/edit_profile.html",
        {"form": form}
    )
def user_logout(request):
    logout(request)
    return redirect("login")
def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            return render(request, "core/login.html", {
                "error": "Invalid username or password"
            })

    return render(request, "core/login.html")
def job_list(request):
    jobs = JobRole.objects.select_related("company").all()

    return render(request, "core/job_list.html", {
        "jobs": jobs
    })
@login_required(login_url="/login/")
def job_detail(request, job_id):
    job = get_object_or_404(JobRole, id=job_id)

    student = get_object_or_404(
        StudentProfile,
        user=request.user
    )

    eligibility = check_eligibility(
        student,
        job
    )

    return render(
        request,
        "core/job_detail.html",
        {
            "job": job,
            "student": student,
            "eligibility": eligibility,
        }
    )
@login_required(login_url="/login/")
def apply_job(request, job_id):
    job = get_object_or_404(JobRole, id=job_id)

    student = get_object_or_404(
        StudentProfile,
        user=request.user
    )

    eligibility = check_eligibility(
        student,
        job
    )

    if not eligibility["eligible"]:
        return redirect("job_detail", job_id=job.id)

    application, created = Application.objects.get_or_create(
    student=student,
    job=job
)

    if created:
        messages.success(
          request,
          "Application submitted successfully!"
         )
    else:
        messages.info(
          request,
           "You have already applied for this job."
        )

    return redirect("job_list")
@login_required(login_url="/login/")
def my_applications(request):
    student = get_object_or_404(
        StudentProfile,
        user=request.user
    )

    applications = Application.objects.filter(
        student=student
    ).select_related("job", "job__company")

    return render(request, "core/my_applications.html", {
        "applications": applications
    })
def admin_required(user):
    return user.is_staff


@user_passes_test(admin_required, login_url="/login/")
def admin_dashboard(request):
    companies_count = Company.objects.count()
    jobs_count = JobRole.objects.count()
    applications_count = Application.objects.count()
    students_count = StudentProfile.objects.count()

    return render(request, "core/admin_dashboard.html", {
        "companies_count": companies_count,
        "jobs_count": jobs_count,
        "applications_count": applications_count,
        "students_count": students_count,
    })
def admin_required(user):
    return user.is_staff


@user_passes_test(admin_required, login_url="/login/")
def admin_dashboard(request):
    companies_count = Company.objects.count()
    jobs_count = JobRole.objects.count()
    applications_count = Application.objects.count()
    students_count = StudentProfile.objects.count()

    return render(request, "core/admin_dashboard.html", {
        "companies_count": companies_count,
        "jobs_count": jobs_count,
        "applications_count": applications_count,
        "students_count": students_count,
    })