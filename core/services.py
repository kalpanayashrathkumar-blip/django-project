def check_eligibility(student, job_role):
    
    cgpa_eligible = student.cgpa >= job_role.minimum_cgpa

    student_skills = set(
        skill.name.lower()
        for skill in student.skills.all()
    )

    
    required_skills = set(
        skill.name.lower()
        for skill in job_role.required_skills.all()
    )

    missing_skills = required_skills - student_skills

   
    skills_eligible = len(missing_skills) == 0

    eligible = cgpa_eligible and skills_eligible

    return {
        "eligible": eligible,
        "cgpa_eligible": cgpa_eligible,
        "skills_eligible": skills_eligible,
        "missing_skills": sorted(missing_skills),
    }
def get_dashboard_data(student):
    from .models import JobRole

    job_roles = JobRole.objects.prefetch_related(
        "required_skills"
    )

    eligible_jobs = 0
    missing_skills = set()

    for job in job_roles:
        result = check_eligibility(student, job)

        if result["eligible"]:
            eligible_jobs += 1

        missing_skills.update(result["missing_skills"])

    return {
        "total_jobs": job_roles.count(),
        "eligible_jobs": eligible_jobs,
        "missing_skills": sorted(missing_skills),
    }
def get_profile_completion(student):
    total_fields = 5
    completed_fields = 0

    if student.phone:
        completed_fields += 1

    if student.college:
        completed_fields += 1

    if student.branch:
        completed_fields += 1

    if student.graduation_year:
        completed_fields += 1

    if student.cgpa:
        completed_fields += 1

    percentage = int(
        (completed_fields / total_fields) * 100
    )

    return {
        "completed_fields": completed_fields,
        "total_fields": total_fields,
        "percentage": percentage,
    }
def get_skill_gap(student):
    from .models import JobRole

    student_skills = set(
        skill.name.lower()
        for skill in student.skills.all()
    )

    required_skills = set()

    job_roles = JobRole.objects.prefetch_related(
        "required_skills"
    )

    for job in job_roles:
        for skill in job.required_skills.all():
            required_skills.add(skill.name.lower())

    missing_skills = required_skills - student_skills

    return sorted(missing_skills)
def get_skill_recommendations(skill_gap):
    recommendations = {
        "python": {
            "reason": "Python is commonly used in backend and data-related roles.",
            "action": "Learn Python fundamentals and build a practical project.",
        },
        "django": {
            "reason": "Django is useful for Python-based web development roles.",
            "action": "Learn Django REST APIs and build a CRUD application.",
        },
        "sql": {
            "reason": "SQL is commonly required for software and data-related roles.",
            "action": "Practice SELECT, JOIN, GROUP BY, subqueries and database design.",
        },
        "javascript": {
            "reason": "JavaScript is widely used for web application development.",
            "action": "Learn JavaScript fundamentals and build an interactive web page.",
        },
        "react": {
            "reason": "React is used for building modern web interfaces.",
            "action": "Learn React fundamentals and build a small frontend project.",
        },
        "git": {
            "reason": "Git is widely used for collaborative software development.",
            "action": "Practice branching, merging, pull requests and conflict resolution.",
        },
    }

    result = []

    for skill in skill_gap:
        recommendation = recommendations.get(
            skill.lower(),
            {
                "reason": "This skill appears in currently listed job requirements.",
                "action": f"Learn {skill} fundamentals and build a small practical project.",
            }
        )

        result.append({
            "skill": skill,
            "reason": recommendation["reason"],
            "action": recommendation["action"],
        })

    return result