student = {
    "name": "Student",
    "cgpa": 9.0,
    "skills": ["Python", "SQL", "HTML", "CSS", "JavaScript"],
    "dsa_solved": 80,
    "projects": 2,
    "preferred_role": "Software Developer"
}

print(student)
print(student["cgpa"])
print(student["skills"])




def calculate_readiness(student):
    score = 0
    if student["cgpa"] >= 8:
        score+=25
    elif student["cgpa"] >= 7:
        score += 20
    else :
        score += 10

    if student["dsa_solved"] >= 150:
        score += 30
    elif student["dsa_solved"] >= 75:
        score += 20 
    else:
        score += 10

    if student["projects"] >= 3:
        score += 25
    elif student["projects"] >= 2:
        score +=20
    else:
        score += 10  
    if student["skills"] == "python" :
       score += 5
    if student["skills"] == "SQL" :
           score += 5
    if student["skills"] == "Git" :
           score += 5
    if student["skills"] == "Cloud" :
           score += 5                 
    else:
        print("no required skills present")             
                                            

                                            
    return score

readiness = calculate_readiness(student)
print("Placement Readiness:" ,readiness, "/100")   

required_skills =[
     "python", "SQL" , "Git","DSA","OOP", "DBMS"
]
skill_gaps =[]
for skill in required_skills:
     if skill not in student["skills"]:
        if skill in ["DSA", "OOP"]:
            priority = "High"
        else:
            priority = "Medium"

        skill_gaps.append({
            "skill": skill,
            "priority": priority
        })

print("Skill Gaps:", skill_gaps)  
print("\nRecommended Learning Order:")

for gap in skill_gaps:
    if gap["priority"] == "High":
        print(f"🔥 Learn {gap['skill']} first — High Priority")
    else:
      print(f"📘 Learn {gap['skill']} next — Medium Priority")   
priority_order = {
    "High": 1,
    "Medium": 2
}

skill_gaps.sort(key=lambda gap: priority_order[gap["priority"]])

print("\nRecommended Learning Order:")

for gap in skill_gaps:
    print(f"{gap['skill']} → {gap['priority']} Priority")         