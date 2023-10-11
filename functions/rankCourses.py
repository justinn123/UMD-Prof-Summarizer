import planetterp

def rankDep(department, level):
    course_names = []
    course_gpa = []
    min = int(level)*100
    max = min+100
    try:
        courses = planetterp.courses(department=department, reviews=False)
    except:
        return None
    course_num = ""

    for x in range(len(courses)-1):
        course_num = str(courses[x]['course_number'])
        course_num = course_num[:3]
        if(int(course_num) < int(min) or int(course_num) > int(max)):
            continue
        if(courses[x]['average_gpa']!= None):
            course_gpa.append(float('{0:.2f}'.format(courses[x]['average_gpa'])))
        else:
            course_gpa.append(0)
        course_name_str = ""
        course_name_str+=(f"{courses[x]['name']} ({courses[x]['title']})")
        course_names.append(course_name_str)

    prof_dictionary = dict(zip(course_names, course_gpa))
    ranked = dict(sorted(prof_dictionary.items(), key = lambda item: item[1],reverse = True))

    counter = 1
    ranked_str = ""

    for key in ranked:
        ranked_str+=(f"{counter}) {key}: {ranked[key]}\n")
        counter+=1
    if len(ranked_str) > 2000:
        ranked_str = ("There are too many courses to display on discord.")
    return(ranked_str)
