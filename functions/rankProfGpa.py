import planetterp

GRADE_WEIGHTS = {
        "A+": 4,
        "A": 4,
        "A-": 3.7,
        "B+": 3.3,
        "B": 3,
        "B-": 2.7,
        "C+": 2.3,
        "C": 2,
        "C-": 1.7,
        "D+": 1.3,
        "D": 1,
        "D-": .7,
        "F": 0,
        "W": 0
    }


def rankByGPA(courseVal):    
    try:
        course = planetterp.course(name = courseVal)
        prof_list = course["professors"]
    except:
        return None
    
    prof_gpa = []
    for x in prof_list:
        gpa = calcGPA(courseVal, x)
        prof_gpa.append(gpa)

    prof_dict = dict(zip(prof_list,prof_gpa))
    ranked = dict(sorted(prof_dict.items(), key=lambda item: item[1], reverse=True))
    ranked_str = ""
    rank = 1
    for key in ranked:
        if(ranked[key] != -1):
            ranked_str+=str(f"{rank}) {key}: {ranked[key]}")
        else:
            ranked_str+=str(f"{rank}) {key}: No Data")
        ranked_str+=("\n")
        rank+=1
    return ranked_str

def calcGPA(courseName, prof):
    try:
        grades = planetterp.grades(course = str(courseName), professor=str(prof))
    except:
        return -1
    counter = 0
    total = 0

    for x in grades:
        for grade, weight in GRADE_WEIGHTS.items():
            total += x[grade] * weight
            counter += x[grade]
            

    if counter != 0:
        average_gpa = total / counter
    else:
        average_gpa = -1
    return float('{0:.2f}'.format(average_gpa))