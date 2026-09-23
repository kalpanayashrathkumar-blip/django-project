from django import forms
from django.contrib.auth.models import User

from .models import StudentProfile,Project


class RegistrationForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ["username", "email"]

    def clean(self):

        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password:

            if password != confirm_password:
                raise forms.ValidationError(
                    "Passwords do not match."
                )

        return cleaned_data


class StudentProfileForm(forms.ModelForm):

    class Meta:
        model = StudentProfile
        fields = [
            "phone",
            "college",
            "branch",
            "graduation_year",
            "cgpa",
             "profile_photo",
            "skills",
            "resume",
        ]
class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = [
            "title",
            "description",
            "technologies",
            "github_link",
        ]        
