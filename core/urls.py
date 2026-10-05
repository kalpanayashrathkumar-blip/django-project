from django.urls import path
from . import views

from .views import user_logout  
from .views import (
    dashboard,
    job_list,
    check_job_eligibility,
    register,
    create_profile,
    add_project,
    delete_project,
    edit_project,
    edit_profile,
)
urlpatterns = [
    
     path(
        "dashboard/",
        views.dashboard,
        name="dashboard"
    ),
       path("jobs/", job_list, name="job_list"),
        path(
        "register/",
        views.register,
        name="register"
    ),
    path(
        "eligibility/<int:job_id>/",
        views.check_job_eligibility,
        name="check_job_eligibility"
    ),
   
   path(
        "profile/create/",
        views.create_profile,
        name="create_profile"
    ),
    path(
    "project/add/",
    views.add_project,
    name="add_project"
), 
path(
    "project/delete/<int:project_id>/",
    views.delete_project,
    name="delete_project"
),
path(
    "project/edit/<int:project_id>/",
    views.edit_project,
    name="edit_project"
),
path(
    "profile/edit/",
    views.edit_profile,
    name="edit_profile"
), 
path("login/", views.user_login, name="login"),
path("logout/", user_logout, name="logout"),
path("jobs/", views.job_list, name="job_list"),
path("jobs/<int:job_id>/", views.job_detail, name="job_detail"),
path(
    "jobs/<int:job_id>/apply/",
    views.apply_job,
    name="apply_job"
),
path(
    "my-applications/",
    views.my_applications,
    name="my_applications"
),
path(
    "admin-dashboard/",
    views.admin_dashboard,
    name="admin_dashboard"
),
path(
    "admin-dashboard/",
    views.admin_dashboard,
    name="admin_dashboard"
),
path("api/students/", views.student_api, name="student_api"),
path("api/companies/", views.company_api, name="company_api"),
path("api/jobs/", views.job_api, name="job_api"),
path(
    "api/jobs/<int:job_id>/eligibility/",
    views.eligibility_api,
    name="eligibility_api",
),
path(
    "api/applications/",
    views.application_api,
    name="application_api",
),
path(
    "api/dashboard/",
    views.dashboard_api,
    name="dashboard_api",
),
path(
    "api/recommendations/",
    views.job_recommendations_api,
    name="job_recommendations_api",
),
path(
    "api/ml/predict/",
    views.ml_prediction_api,
    name="ml_prediction_api"
),
path(
    "recommended-jobs/",
    views.recommended_jobs,
    name="recommended_jobs",
),
path(
    "skill-gap/",
    views.skill_gap_view,
    name="skill_gap_view",
),
]