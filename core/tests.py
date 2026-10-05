   

from django.contrib.auth.models import User
from django.test import TestCase

from .models import Company, JobRole, Skill, StudentProfile
from .services import check_eligibility
from .services import calculate_job_match_score ,get_skill_gap, get_skill_recommendations, get_dashboard_data
from unittest.mock import patch

class EligibilityTest(TestCase):

    def test_student_is_eligible_for_job(self):
        user = User.objects.create_user(
            username="teststudent",
            password="testpass123"
        )

        student = StudentProfile.objects.create(
            user=user,
            cgpa=8.5,
            graduation_year=2026,
        )

        skill = Skill.objects.create(name="Python")
        student.skills.add(skill)

        company = Company.objects.create(name="Test Company")

        job = JobRole.objects.create(
            company=company,
            title="Python Developer",
            minimum_cgpa=7.0,
        )

        job.required_skills.add(skill)

        result = check_eligibility(student, job)

        self.assertTrue(result["eligible"])

    def test_student_is_not_eligible_when_skill_is_missing(self):
        user = User.objects.create_user(
            username="teststudent2",
            password="testpass123"
        )

        student = StudentProfile.objects.create(
            user=user,
            cgpa=8.5,
            graduation_year=2026,
        )

        required_skill = Skill.objects.create(name="Django")

        company = Company.objects.create(name="Test Company 2")

        job = JobRole.objects.create(
            company=company,
            title="Django Developer",
            minimum_cgpa=7.0,
        )

        job.required_skills.add(required_skill)

        result = check_eligibility(student, job)

        self.assertFalse(result["eligible"])
        self.assertIn("django", result["missing_skills"])
class JobMatchScoreTest(TestCase):

    def test_job_match_score(self):
        user = User.objects.create_user(
            username="matchstudent",
            password="testpass123"
        )

        student = StudentProfile.objects.create(
            user=user,
            cgpa=8.5,
            graduation_year=2026,
        )

        python_skill = Skill.objects.create(name="Python")
        django_skill = Skill.objects.create(name="Django")

        student.skills.add(python_skill)

        company = Company.objects.create(name="Match Company")

        job = JobRole.objects.create(
            company=company,
            title="Backend Developer",
            minimum_cgpa=7.0,
        )

        job.required_skills.add(
            python_skill,
            django_skill,
        )

        score = calculate_job_match_score(student, job)

        self.assertGreater(score, 0)
        self.assertLessEqual(score, 100)   
class MLPlacementTest(TestCase):

    @patch("core.ml_models.load_placement_model")
    def test_predict_placement(self, mock_load):
        from sklearn.ensemble import RandomForestClassifier
        import pandas as pd

        user = User.objects.create_user(
            username="mlstudent",
            password="testpass123"
        )

        student = StudentProfile.objects.create(
            user=user,
            cgpa=8.5,
            graduation_year=2026,
        )

        model = RandomForestClassifier(n_estimators=10, random_state=42)

        training_data = pd.DataFrame([
            {
                "cgpa": 8.0,
                "skill_count": 2,
                "project_count": 1,
                "application_count": 2,
            },
            {
                "cgpa": 9.0,
                "skill_count": 4,
                "project_count": 3,
                "application_count": 4,
            },
        ])

        target = [False, True]

        model.fit(training_data, target)

        mock_load.return_value = (model, 1.0)

        from core.ml_models import predict_placement

        result = predict_placement(student)

        self.assertIn("placement_prediction", result)
        self.assertIn("confidence", result)
        self.assertIn("model_accuracy", result)          
class SkillGapTest(TestCase):

    def test_skill_gap_and_recommendation(self):
        user = User.objects.create_user(
            username="skillstudent",
            password="testpass123"
        )

        student = StudentProfile.objects.create(
            user=user,
            cgpa=8.0,
            graduation_year=2026,
        )

        company = Company.objects.create(name="Skill Company")

        job = JobRole.objects.create(
            company=company,
            title="Django Developer",
            minimum_cgpa=7.0,
        )

        django = Skill.objects.create(name="Django")
        job.required_skills.add(django)

        skill_gap = get_skill_gap(student)

        self.assertIn("django", skill_gap)

        recommendations = get_skill_recommendations(skill_gap)

        self.assertEqual(recommendations[0]["skill"], "django") 
class DashboardDataTest(TestCase):

    def test_dashboard_data(self):
        user = User.objects.create_user(
            username="dashboardstudent",
            password="testpass123"
        )

        student = StudentProfile.objects.create(
            user=user,
            cgpa=8.5,
            graduation_year=2026,
        )

        company = Company.objects.create(
            name="Dashboard Company"
        )

        JobRole.objects.create(
            company=company,
            title="Software Developer",
            minimum_cgpa=7.0,
        )

        data = get_dashboard_data(student)

        self.assertIn("total_jobs", data)
        self.assertIn("eligible_jobs", data)
        self.assertIn("missing_skills", data)

        self.assertEqual(data["total_jobs"], 1)
        self.assertEqual(data["eligible_jobs"], 1)                  
