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
]